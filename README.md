# RecipeFinder

**RecipeFinder** is a smart kitchen assistant that helps you decide what to cook based on what you already have in your fridge.  
The project uses **object detection** to recognize ingredients from a photo you take of your fridge or kitchen items, then suggests relevant recipes you can make from them. The system includes a lightweight user interface and a custom-trained YOLOv8 model to identify food items and match them with recipes from a dataset.

---

## Setup
- Install Ultralytics by entering `pip install ultralytics` into Command Prompt
- Make sure your Python version is between **3.8–3.11**  
  You can check your version with `python --version` in Command Prompt
- Run `main.py`
- Bimbam code go brrrr 🚀

---

## File Description
- **RecipeFinder_Tamm&Põldma.ipynb** – Insight into our development process
- **Report.pdf** – Report about this project
- **best.pt** – Our trained object detection model weights (YOLOv8)
- **edited_recipes.csv** – Holds recipes filtered based on detected ingredients
- **main.py** – Main program file with the UI
- **recipes.csv** – Full dataset of recipe data

---

Built by **Sander Põldma** and **Kristian Tamm**  
University of Tartu
