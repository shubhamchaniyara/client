import os
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    ViltProcessor,
    ViltForQuestionAnswering,
    Trainer,
    TrainingArguments,
    DefaultDataCollator,
)
import matplotlib.pyplot as plt


def load_model(num_labels):
    try:
        processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
        model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

       
        model.classifier = torch.nn.Linear(model.classifier.in_features, num_labels)
        return model, processor
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None


class BirdDataset(Dataset):
    def __init__(self, image_paths, questions, labels, processor, image_size=(384, 384)):
        self.image_paths = image_paths
        self.questions = questions
        self.labels = labels
        self.processor = processor
        self.image_size = image_size

    def __getitem__(self, idx):
        
        image = Image.open(self.image_paths[idx]).convert("RGB")
       
        image = image.resize(self.image_size)

        
        encoding = self.processor(
            images=image,
            text=self.questions[idx],
            return_tensors="pt",
            padding=True,
            truncation=True
        )

       
        encoding["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)

        return encoding

    def __len__(self):
        return len(self.image_paths)


def display_image_with_answer(image_path, answer):
    image = Image.open(image_path).convert("RGB")
    plt.imshow(image)
    plt.title(f"Predicted answer: {answer}")
    plt.axis("off")
    plt.show()


def load_dataset(base_path):
    image_paths = []
    questions = []
    labels = []

    images_folder = os.path.join(base_path, "images")
    classes_file = os.path.join(base_path, "classes.txt")

    
    try:
        with open(classes_file, "r") as f:
            for line in f:
                
                parts = line.strip().split(" ", 1)

                if len(parts) != 2:
                    continue  
                label_str, class_name = parts
                label = int(label_str) - 1 

                folder_path = os.path.join(images_folder, class_name)

                
                if os.path.exists(folder_path):
                    
                    for img_file in os.listdir(folder_path):
                        img_file_path = os.path.join(folder_path, img_file)

                        
                        if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                            image_paths.append(img_file_path)
                            questions.append("Which bird is in the image?")
                            labels.append(label)

                else:
                    print(f"Warning: Folder '{folder_path}' not found.")

    except FileNotFoundError:
        print(f"Error: '{classes_file}' not found. Please check the file path.")

    return image_paths, questions, labels


def main():
    base_path = "../../image/CUB_200_2011"

    
    image_paths, questions, labels = load_dataset(base_path)
    if len(image_paths) == 0:
        print("No images loaded. Please check the dataset paths.")
        return

    num_labels = 199  
    model, processor = load_model(num_labels)
    if model is None or processor is None:
        return

    split_index = int(0.8 * len(image_paths))
    train_image_paths, val_image_paths = image_paths[:split_index], image_paths[split_index:]
    train_questions, val_questions = questions[:split_index], questions[split_index:]
    train_labels, val_labels = labels[:split_index], labels[split_index:]

   
    train_dataset = BirdDataset(train_image_paths, train_questions, train_labels, processor)
    val_dataset = BirdDataset(val_image_paths, val_questions, val_labels, processor)

  
    data_collator = DefaultDataCollator()

   
    train_dataloader = DataLoader(train_dataset, batch_size=8, shuffle=True, collate_fn=data_collator)
    val_dataloader = DataLoader(val_dataset, batch_size=8, collate_fn=data_collator)

    
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
        logging_dir="./logs",
        logging_steps=10,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator,
    )

    
    trainer.train()

    
    model.save_pretrained("./vilt-finetuned-birds")

    display_image_with_answer(val_image_paths[0], "Sample Prediction")

if __name__ == "__main__":
    main()
