import tkinter as tk
from tkinter import filedialog
import webbrowser
# import onnxruntime as rt
import pip
from ultralytics import YOLO
import pandas as pd
from tkinter import ttk
import urllib

class_dict = {0: 'apple', 1: 'chicken', 2: 'egg', 3: 'garlic', 4: 'ginger', 5: 'lemon', 6: 'lettuce', 7: 'onion',
              8: 'pepper', 9: 'potato', 10: 'tomato'}


def UploadAction(event=None):
    filepath = filedialog.askopenfilename()
    print('Selected:', filepath)
    predict(filepath)


def callback(url):
    webbrowser.open_new(url)


def predict(filepath):
    ingredient_dict = pd.read_pickle('ingr_map.pkl')
    model = YOLO("best.pt")
    results = model(filepath, save_txt=True)
    print(results)
    filename = filepath.split("/")[-1].split(".")[0]
    print(filename)
    # We expect everyone to have oil salt sugar at home
    everyone_has = ['oil', 'salt', 'sugar']
    detected_classes = read_detections(filename)  # .extend(everyone_has)
    print(detected_classes)
    find_recipe(set(detected_classes), ingredient_dict)
    display_found_recipes(ingredient_dict)


def read_detections(filename):
    with open("runs/detect/predict/labels/" + filename + ".txt", 'r') as file:
        lines = file.readlines()
    detected_classes = [line.split()[0] for line in lines]
    for i in range(len(detected_classes)):
        ind = detected_classes[i]
        detected_classes[i] = class_dict[int(ind)]
    return detected_classes


def is_subset_general(main_set, subset, percent):
    count = 0
    for element in subset:
        if element in main_set:
            count += 1
        else:
            for main_element in main_set:
                if element in main_element or main_element in element:
                    count += 1
    if count / len(subset) >= percent:
        return True
    return False


def find_recipe(target_ingredients, ingredient_dict):
    data = pd.read_csv('recipes.csv')
    recipe_df = pd.DataFrame(data)

    # Initialize a list to store the selected rows
    selected_rows = []

    # Iterate through each row in the DataFrame
    for index, row in recipe_df.iterrows():
        ingredient_set = set(row.ingredients)

        if is_subset_general(target_ingredients, ingredient_set, 0.5):
            selected_rows.append(row)

    found_recipes_df = pd.DataFrame(selected_rows)
    found_recipes_df.to_csv('edited_recipes.csv', index=False)


def display_found_recipes(ingredient_dict):
    data = pd.read_csv('edited_recipes.csv')
    recipe_df = pd.DataFrame(data)
    if recipe_df.empty:
        not_found = tk.Label(root,
                             text="We did not find any recipes for your ingredients. Try with a different picture.",
                             font=('helvetica now', 12, 'bold'),
                             background=backcolor)
        not_found.pack()
    else:
        info = tk.Label(root, text="Click on a link to see recipe.", font=('helvetica now', 12, 'bold'), background=backcolor)
        info.pack()
        # Define the headings
        tree.heading("recipe_name", text="Recipe Name")
        tree.heading("recipe_link", text="Recipe Link")
        tree.heading("recipe_ingredients", text="Recipe Ingredients")

        # Define the column widths
        tree.column("recipe_name", width=150)
        tree.column("recipe_link", width=250)
        tree.column("recipe_ingredients", width=300)

        for index, row in recipe_df.iterrows():
            recipe_name = row['name']
            recipe_id = row['id']
            recipe_ingredients = row['ingredients']
            recipe_link = "www.food.com/recipe/" + recipe_name.replace(" ", "-") + "-" + str(recipe_id)
            tree.insert("", tk.END, values=(recipe_name, recipe_link, recipe_ingredients))

        tree.bind("<Button-1>", click)

        tree.pack(fill=tk.BOTH, expand=True)


def click(event):
    link = tree.item(tree.identify_row(event.y), "values")[1]
    print('Opening link: '+link)
    webbrowser.open(link, new=1)


backcolor = 'pink'
# Create the main window
root = tk.Tk()
root.geometry("450x600")
root.title("Recipe Finder")
root.configure(background=backcolor)

columns = ("recipe_name", "recipe_link", "recipe_ingredients")
tree = ttk.Treeview(root, columns=columns, show="headings")

# Add a heading label with some padding and styling
heading = tk.Label(root, text="Recipe Finder", font=('helvetica now', 24, 'bold'), background=backcolor)
heading.pack()

# Add names label
names = tk.Label(root, text="Kristian Tamm & Sander Põldma", font=('helvetica now', 12), background=backcolor)
names.pack()

# Add description
text1 = tk.Label(root, text="Welcome to our Recipe Finder!", font=('helvetica now', 12, 'bold'), background=backcolor)
text1.pack(pady=(35, 0))

# Create the Label inside the LabelFrame
text2 = tk.Label(root, text="Simply upload a photo of your food ingredients, "
                            "and our AI will identify them and suggest delicious "
                            "recipes you can make with what you have at home.",
                 font=('helvetica now', 12), wraplength=360, background=backcolor)
text2.pack()

# Add a link to YouTube with proper padding and alignment
# link_frame = tk.Frame(root)
# link_frame.pack(pady=20)
# link1 = tk.Label(link_frame, text="YouTube", fg="blue", cursor="hand2", font=('helvetica now', 14))
# link1.pack()
# link1.bind("<Button-1>", lambda e: callback("http://www.youtube.com"))

# Add a button to upload files with some padding
button = tk.Button(root, text='Upload File Here', command=UploadAction, font=('helvetica now', 14), padx=20, pady=10)
button.pack(pady=20)

# Run the main event loop
root.mainloop()
