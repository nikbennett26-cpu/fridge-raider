import streamlit as st
import re

# --- PAGE CONFIG ---
st.set_page_config(page_title="Kitchen Sync", layout="wide", page_icon="🔄")

# --- THEME MANAGEMENT ---
with st.sidebar:
    st.title("🔄 Kitchen Sync")
    st.caption("Get in sync with your ingredients.")
    st.write("---")
    dark_mode = st.toggle("🌙 Dark Mode", value=False)

# --- DEFINE CSS THEMES ---

# 1. LIGHT THEME (Modern "Pop" UI)
light_theme_css = """
<style>
    :root { color-scheme: light; }
    .stApp { background-color: #f0f4f8 !important; } /* Slightly cooler grey background */
    
    /* Text Colors */
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, textarea, .stMarkdown {
        color: #1e293b !important;
        font-family: 'Inter', system-ui, sans-serif;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #ffffff !important; border-right: none; box-shadow: 2px 0 10px rgba(0,0,0,0.05); }
    
    /* Inputs */
    .stTextArea textarea {
        background-color: #f8fafc !important;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
    }
    .stTextArea textarea:focus { border-color: #0d9488 !important; }
    
    /* --- TABS (The "Pill" Style - No Underline) --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px; /* Space between tabs */
        margin-bottom: 16px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: 2px solid transparent; /* Reserve space for no jumping */
        color: #64748b;
        font-weight: 600;
        border-radius: 50px; /* Pill shape */
        padding: 6px 16px;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #e0f2fe !important; /* Light blue pill bg */
        color: #0369a1 !important; /* Dark blue text */
        border: 2px solid #bae6fd !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
         background-color: #f1f5f9;
         color: #334155;
    }
    
    /* --- CARD DESIGN (Stand Out!) --- */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        /* Thicker, clearer border */
        border: 2px solid #e2e8f0 !important;
        /* Keep the accent, but make it a gradient strip */
        border-top: 6px solid #0d9488 !important; 
        /* Much rounder corners */
        border-radius: 20px !important;
        /* More breathing room */
        padding: 24px !important;
        /* Deep, soft shadow for "lift" */
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 20px 35px -5px rgba(0, 0, 0, 0.15), 0 10px 15px -5px rgba(0, 0, 0, 0.1) !important;
        border-top-color: #3b82f6 !important; /* Color shift on hover */
    }

    /* Badges */
    .have-tag { background-color: #dcfce7; color: #14532d; border: 1px solid #86efac; font-weight: 700; }
    .missing-tag { background-color: #f1f5f9; color: #64748b; border: 1px solid #cbd5e1; }
</style>
"""

# 2. DARK THEME
dark_theme_css = """
<style>
    :root { color-scheme: dark; }
    .stApp { background-color: #0b1120 !important; }
    
    /* Text Colors */
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, textarea, .stMarkdown {
        color: #e2e8f0 !important;
        font-family: 'Inter', system-ui, sans-serif;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #111827 !important; border-right: 1px solid #1f2937; }
    
    /* Inputs */
    .stTextArea textarea {
        background-color: #1f2937 !important;
        color: #e2e8f0 !important;
        border: 2px solid #374151;
        border-radius: 12px;
    }
    
    /* --- TABS (Dark Pill Style) --- */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; margin-bottom: 16px; }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: 2px solid transparent;
        color: #9ca3af;
        font-weight: 600;
        border-radius: 50px;
        padding: 6px 16px;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #1e293b !important;
        color: #2dd4bf !important;
        border: 2px solid #2dd4bf !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
    }
    
    /* --- CARD DESIGN (Dark Stand Out) --- */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #1f2937;
        border: 2px solid #374151 !important;
        border-top: 6px solid #2dd4bf !important;
        border-radius: 20px !important;
        padding: 24px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-5px) scale(1.01);
        background-color: #273548;
        box-shadow: 0 20px 40px -5px rgba(0, 0, 0, 0.6);
    }

    /* Badges */
    .have-tag { background-color: #065f46; color: #d1fae5; border: 1px solid #059669; font-weight: 700; }
    .missing-tag { background-color: #374151; color: #9ca3af; border: 1px solid #4b5563; }
    
    /* Icons/Containers */
    button[kind="header"] { color: white !important; }
    .streamlit-expanderHeader { background-color: transparent !important; color: inherit !important; }
</style>
"""

# --- INJECT CSS ---
if dark_mode:
    st.markdown(dark_theme_css, unsafe_allow_html=True)
else:
    st.markdown(light_theme_css, unsafe_allow_html=True)

# --- GLOBAL STYLES ---
st.markdown("""
<style>
    .have-tag, .missing-tag {
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin: 3px;
        letter-spacing: 0.5px;
    }
    h3 {
        font-weight: 800 !important;
        font-size: 1.5rem !important;
        margin-bottom: 0.2rem !important;
        padding-top: 0 !important;
        letter-spacing: -0.5px;
    }
    .recipe-time {
        font-size: 0.9rem;
        font-weight: 600;
        opacity: 0.7;
        margin-bottom: 12px;
        display: block;
    }
    .sidebar-tag {
        background-color: #e0f2fe; 
        color: #0369a1; 
        border: 1px solid #7dd3fc;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)


# --- MAIN CONTENT ---
st.title("Kitchen Sync")
st.markdown("### 🍳 Everything but the... waste.")
st.write("Enter the ingredients you already have at home, and we'll find the perfect recipe for you.")

# --- LOGIC ---
NON_VEGAN_ITEMS = {
    "eggs", "cheese", "butter", "milk", "chicken", "beef", "bacon", "tuna", 
    "salmon", "shrimp", "honey", "cream cheese", "yogurt", "mayo", "ground beef", 
    "parmesan", "mozzarella", "feta"
}

# --- THE RECIPE DATABASE ---
recipes = [
    # --- 1. EMPTY FRIDGE / PANTRY STAPLES ---
    {
        "name": "Beans on Toast 🇬🇧",
        "ingredients": {"bread", "baked beans", "butter"},
        "instructions": "Toast the bread. Microwave or heat beans on stove. Butter toast heavily. Pour beans over.",
        "time": "5 mins", "one_pot": True
    },
    {
        "name": "Cheese Quesadilla 🧀",
        "ingredients": {"tortilla", "cheese", "butter"},
        "instructions": "Melt butter in pan. Add tortilla. Sprinkle cheese. Fold in half. Cook until crispy and melted.",
        "time": "5 mins", "one_pot": True
    },
    {
        "name": "Tuna Pasta 🐟",
        "ingredients": {"pasta", "tuna", "mayo", "corn", "black pepper"},
        "instructions": "Boil pasta. Drain. Mix in canned tuna, mayo, and corn while hot. Season generously.",
        "time": "12 mins", "one_pot": True
    },
    {
        "name": "Jacket Potato 🥔",
        "ingredients": {"potatoes", "butter", "cheese", "salt", "pepper"},
        "instructions": "Prick potato. Microwave 5-8 mins until soft. Cut open, fluff inside, add butter and cheese.",
        "time": "10 mins", "one_pot": True
    },
    {
        "name": "Cinnamon Sugar Toast 🍞",
        "ingredients": {"bread", "butter", "sugar", "cinnamon"},
        "instructions": "Toast bread. Butter immediately. Sprinkle heavily with sugar and cinnamon mix.",
        "time": "3 mins", "one_pot": True
    },
    {
        "name": "Peanut Butter & Banana 🍌",
        "ingredients": {"bread", "peanut butter", "banana"},
        "instructions": "Toast bread. Spread peanut butter. Top with sliced banana. Optional: Drizzle honey.",
        "time": "3 mins", "one_pot": True
    },
    {
        "name": "Buttered Sweet Corn 🌽",
        "ingredients": {"corn", "butter", "salt", "pepper"},
        "instructions": "Boil or steam corn. Toss generously with butter, salt, and pepper.",
        "time": "10 mins", "one_pot": True
    },
    {
        "name": "Cheesy Rice 🍚",
        "ingredients": {"rice", "cheese", "butter", "milk", "salt"},
        "instructions": "Mix hot cooked rice with butter, milk, and cheese until melted and creamy.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "Egg in a Hole 🍞",
        "ingredients": {"bread", "eggs", "butter", "salt"},
        "instructions": "Cut a hole in the bread. Fry bread in butter. Crack egg into the hole. Cook until set.",
        "time": "10 mins", "one_pot": True
    },
    {
        "name": "Garlic Sautéed Mushrooms 🍄",
        "ingredients": {"mushrooms", "butter", "garlic", "soy sauce", "parsley"},
        "instructions": "Sauté mushrooms in butter until browned. Add garlic and soy sauce. Cook 2 mins.",
        "time": "12 mins", "one_pot": True
    },
    {
        "name": "Pasta Aglio e Olio 🍝",
        "ingredients": {"pasta", "olive oil", "garlic", "chili flakes", "parsley"},
        "instructions": "Sauté garlic and chili in generous oil. Toss with cooked pasta and pasta water.",
        "time": "15 mins", "one_pot": False
    },
     {
        "name": "Tomato & Onion Scramble 🍳",
        "ingredients": {"eggs", "tomato", "onion", "butter", "salt"},
        "instructions": "Sauté onion and tomato in butter. Add beaten eggs and scramble until cooked.",
        "time": "10 mins", "one_pot": True
    },

    # --- 2. VEGAN SPECIALS 🌱 ---
    {
        "name": "Spicy Peanut Noodles 🍜",
        "ingredients": {"pasta", "peanut butter", "soy sauce", "garlic", "chili flakes", "lime"},
        "instructions": "Boil pasta. Mix peanut butter, soy sauce, garlic, chili, lime, and a splash of pasta water. Toss.",
        "time": "15 mins", "one_pot": False
    },
    {
        "name": "Lentil Soup 🥣",
        "ingredients": {"lentils", "carrots", "onion", "vegetable broth", "garlic", "spinach"},
        "instructions": "Sauté veggies. Add lentils and broth. Simmer 20 mins until soft. Stir in spinach.",
        "time": "30 mins", "one_pot": True
    },
    {
        "name": "Chickpea Smash Sandwich 🥪",
        "ingredients": {"chickpeas", "avocado", "lemon", "bread", "onion", "salt"},
        "instructions": "Mash chickpeas and avocado together with lemon and onion. Spread on toasted bread.",
        "time": "10 mins", "one_pot": False
    },
    {
        "name": "Black Bean Tacos 🌮",
        "ingredients": {"black beans", "corn", "tortilla", "avocado", "salsa", "lime"},
        "instructions": "Warm beans and corn. Fill tortillas. Top with avocado slices, salsa, and lime juice.",
        "time": "15 mins", "one_pot": True
    },
    {
        "name": "Roasted Veggie Bowl 🥗",
        "ingredients": {"sweet potato", "broccoli", "rice", "olive oil", "tahini", "lemon"},
        "instructions": "Roast veggies at 400F. Serve over rice. Drizzle with tahini mixed with lemon.",
        "time": "35 mins", "one_pot": False
    },
    {
        "name": "Garlic Green Beans 🥒",
        "ingredients": {"green beans", "olive oil", "garlic", "lemon", "almonds"},
        "instructions": "Blanch beans. Sauté garlic in oil. Toss beans in mix. Top with lemon/almonds.",
        "time": "15 mins", "one_pot": True
    },
    {
        "name": "Crispy Potato Wedges 🥔",
        "ingredients": {"potatoes", "oil", "paprika", "salt", "garlic"},
        "instructions": "Cut potatoes into wedges. Toss with oil and spices. Bake 400F for 30-35 mins.",
        "time": "40 mins", "one_pot": True
    },
    {
        "name": "Roasted Butternut Squash 🍠",
        "ingredients": {"butternut squash", "olive oil", "cinnamon", "maple syrup", "salt"},
        "instructions": "Cube squash. Toss with oil, cinnamon, syrup, salt. Roast 400F for 30 mins.",
        "time": "35 mins", "one_pot": True
    },

    # --- 3. THE CLASSICS (Vegetarian & Meat) ---
    {
        "name": "Roasted Brussels Sprouts 🥬",
        "ingredients": {"brussels sprouts", "olive oil", "balsamic vinegar", "honey", "salt"},
        "instructions": "Halve sprouts. Toss with oil, balsamic, honey, salt. Roast 400F for 20-25 mins until crispy.",
        "time": "30 mins", "one_pot": True
    },
    {
        "name": "Kale & Apple Salad 🥗",
        "ingredients": {"kale", "apple", "walnuts", "lemon", "olive oil", "parmesan"},
        "instructions": "Massage kale with oil/lemon. Toss with sliced apples, toasted walnuts, and shaved parm.",
        "time": "15 mins", "one_pot": False
    },
    {
        "name": "Cabbage Stir Fry 🥬",
        "ingredients": {"cabbage", "soy sauce", "garlic", "ginger", "sesame oil", "carrot"},
        "instructions": "Sauté garlic/ginger. Add shredded cabbage and carrot. Stir fry 5 mins. Finish with soy sauce/sesame oil.",
        "time": "15 mins", "one_pot": True
    },
    {
        "name": "Spinach Chickpea Curry 🥘",
        "ingredients": {"spinach", "chickpeas", "coconut milk", "curry paste", "onion", "tomato"},
        "instructions": "Sauté onion. Add curry paste/tomatoes. Add chickpeas/milk. Simmer. Stir in spinach at the end.",
        "time": "25 mins", "one_pot": True
    },
    {
        "name": "Honey Glazed Carrots 🥕",
        "ingredients": {"carrots", "honey", "butter", "parsley", "salt"},
        "instructions": "Boil carrots until tender. Drain. Toss in pan with melted butter and honey. Top with parsley.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "Stuffed Mushrooms 🍄",
        "ingredients": {"mushrooms", "cream cheese", "garlic", "spinach", "breadcrumbs"},
        "instructions": "Remove stems. Mix cream cheese, garlic, chopped spinach. Fill caps. Top with breadcrumbs. Bake 375F for 20m.",
        "time": "30 mins", "one_pot": True
    },
    {
        "name": "Corn & Tomato Salad 🌽",
        "ingredients": {"corn", "tomato", "onion", "basil", "olive oil", "lime"},
        "instructions": "Combine corn, diced tomato, onion, basil. Dress with olive oil and lime juice.",
        "time": "10 mins", "one_pot": False
    },
    {
        "name": "Broccoli Cheddar Soup 🥦",
        "ingredients": {"broccoli", "cheese", "milk", "broth", "onion", "flour"},
        "instructions": "Sauté onion. Add flour/milk/broth to thicken. Add broccoli, simmer until soft. Stir in cheese.",
        "time": "25 mins", "one_pot": True
    },
    {
        "name": "Classic Omelette 🍳",
        "ingredients": {"eggs", "cheese", "butter", "salt"},
        "instructions": "Whisk eggs, melt butter, cook until fluffy, add cheese.",
        "time": "10 mins", "one_pot": True
    },
    {
        "name": "Fluffy Pancakes 🥞",
        "ingredients": {"eggs", "milk", "flour", "butter", "sugar"},
        "instructions": "Mix dry and wet ingredients separately, combine, and fry in butter.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "French Toast 🍞",
        "ingredients": {"bread", "eggs", "milk", "cinnamon", "butter"},
        "instructions": "Dip bread in egg/milk mix, fry in butter until golden brown.",
        "time": "15 mins", "one_pot": True
    },
    {
        "name": "Oatmeal Bowl 🥣",
        "ingredients": {"oats", "milk", "honey", "banana", "cinnamon"},
        "instructions": "Cook oats in milk, top with sliced banana and honey.",
        "time": "10 mins", "one_pot": True
    },
    {
        "name": "Avocado Toast with Egg 🥑",
        "ingredients": {"bread", "avocado", "eggs", "chili flakes", "lemon"},
        "instructions": "Toast bread, smash avocado with lemon. Top with fried/poached egg and chili.",
        "time": "10 mins", "one_pot": True
    },
    {
        "name": "Veggie Breakfast Hash 🥔",
        "ingredients": {"potatoes", "bell pepper", "onion", "eggs", "oil"},
        "instructions": "Dice potatoes, peppers, and onions. Fry until soft/crispy. Crack eggs on top and steam until set.",
        "time": "25 mins", "one_pot": True
    },
    {
        "name": "Grilled Cheese Sandwich 🥪",
        "ingredients": {"bread", "cheese", "butter"},
        "instructions": "Butter bread, place cheese inside, grill until golden.",
        "time": "10 mins", "one_pot": True
    },
    {
        "name": "BLT Sandwich 🥓",
        "ingredients": {"bread", "bacon", "lettuce", "tomato", "mayo"},
        "instructions": "Cook bacon, toast bread, layer ingredients with mayo.",
        "time": "15 mins", "one_pot": True
    },
    {
        "name": "Classic Tuna Salad 🐟",
        "ingredients": {"tuna", "mayo", "onion", "celery", "bread"},
        "instructions": "Mix tuna, mayo, diced onion and celery. Serve on bread or lettuce.",
        "time": "10 mins", "one_pot": False
    },
    {
        "name": "Caesar Salad 🥗",
        "ingredients": {"lettuce", "croutons", "parmesan", "chicken", "dressing"},
        "instructions": "Toss lettuce with dressing, top with grilled chicken and croutons.",
        "time": "20 mins", "one_pot": False
    },
    {
        "name": "Greek Salad 🇬🇷",
        "ingredients": {"cucumber", "tomato", "feta", "olives", "onion", "olive oil"},
        "instructions": "Chop veggies roughly. Toss with olive oil and top with block of feta.",
        "time": "15 mins", "one_pot": False
    },
    {
        "name": "Caprese Salad 🇮🇹",
        "ingredients": {"tomato", "mozzarella", "basil", "olive oil", "balsamic vinegar"},
        "instructions": "Slice tomatoes and cheese, arrange with basil, drizzle with oil.",
        "time": "10 mins", "one_pot": False
    },
    {
        "name": "Hummus & Veggies 🥕",
        "ingredients": {"chickpeas", "lemon", "garlic", "olive oil", "tahini", "carrots"},
        "instructions": "Blend chickpeas, lemon, garlic, tahini and oil. Serve with carrot sticks.",
        "time": "15 mins", "one_pot": False
    },
    {
        "name": "Quinoa Salad 🥣",
        "ingredients": {"quinoa", "cucumber", "tomato", "lemon", "feta", "parsley"},
        "instructions": "Cook quinoa. Mix with chopped veggies, crumbled feta, lemon juice and herbs.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "Zucchini Fritters 🥒",
        "ingredients": {"zucchini", "flour", "eggs", "cheese", "garlic", "oil"},
        "instructions": "Grate zucchini and squeeze out water. Mix with flour, egg, cheese. Fry spoonfuls in oil until crispy.",
        "time": "25 mins", "one_pot": True
    },
    {
        "name": "Tomato Pasta 🍝",
        "ingredients": {"pasta", "tomato sauce", "garlic", "olive oil"},
        "instructions": "Boil pasta, sauté garlic in oil, add sauce, mix.",
        "time": "15 mins", "one_pot": False
    },
    {
        "name": "Pesto Pasta 🍃",
        "ingredients": {"pasta", "pesto", "parmesan", "cherry tomatoes"},
        "instructions": "Boil pasta. Save some pasta water. Toss pasta with pesto and a splash of water. Top with tomatoes.",
        "time": "15 mins", "one_pot": False
    },
    {
        "name": "Garlic Butter Shrimp 🍤",
        "ingredients": {"shrimp", "butter", "garlic", "lemon", "parsley"},
        "instructions": "Sauté garlic in butter. Add shrimp, cook 3 mins. Finish with lemon/parsley.",
        "time": "15 mins", "one_pot": True
    },
    {
        "name": "Chicken Stir Fry 🥡",
        "ingredients": {"chicken", "rice", "soy sauce", "vegetables", "oil"},
        "instructions": "Cook chicken, add veggies, stir in sauce, serve over rice.",
        "time": "25 mins", "one_pot": True
    },
    {
        "name": "Tofu Stir Fry 🥦",
        "ingredients": {"tofu", "soy sauce", "ginger", "garlic", "broccoli", "rice"},
        "instructions": "Press tofu, cube, and fry. Remove. Fry aromatics and broccoli. Combine with sauce over rice.",
        "time": "30 mins", "one_pot": True
    },
    {
        "name": "Beef & Broccoli 🥦",
        "ingredients": {"beef", "broccoli", "soy sauce", "garlic", "rice", "sugar"},
        "instructions": "Sear beef strips. Steam broccoli. Toss both in soy/garlic/sugar sauce. Serve over rice.",
        "time": "25 mins", "one_pot": True
    },
    {
        "name": "Spaghetti Carbonara 🇮🇹",
        "ingredients": {"pasta", "eggs", "cheese", "bacon", "black pepper"},
        "instructions": "Boil pasta. Fry bacon. Mix eggs and cheese. Toss hot pasta with egg mix (off heat).",
        "time": "20 mins", "one_pot": False
    },
    {
        "name": "Simple Tacos 🌮",
        "ingredients": {"tortilla", "ground beef", "cheese", "lettuce", "salsa"},
        "instructions": "Cook meat, fill tortillas, top with cheese and salsa.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "Black Bean Burrito 🌯",
        "ingredients": {"tortilla", "black beans", "rice", "cheese", "salsa", "corn"},
        "instructions": "Warm beans and corn. Layer rice, beans, corn, and cheese in tortilla. Roll and serve.",
        "time": "15 mins", "one_pot": False
    },
    {
        "name": "Chicken Curry 🍛",
        "ingredients": {"chicken", "curry paste", "coconut milk", "rice", "onion"},
        "instructions": "Fry onion and chicken, add paste, pour in milk, simmer. Serve with rice.",
        "time": "30 mins", "one_pot": True
    },
    {
        "name": "Fried Rice 🍚",
        "ingredients": {"rice", "eggs", "soy sauce", "peas", "carrots", "oil"},
        "instructions": "Fry veggies, push to side, scramble eggs, add rice and sauce, mix high heat.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "Homemade Pizza 🍕",
        "ingredients": {"flour", "yeast", "tomato sauce", "cheese", "pepperoni"},
        "instructions": "Make dough, add sauce and toppings, bake at high heat (450F) for 12 mins.",
        "time": "45 mins", "one_pot": True
    },
    {
        "name": "Mac & Cheese 🧀",
        "ingredients": {"pasta", "cheese", "milk", "butter", "flour"},
        "instructions": "Make a roux with flour/butter, add milk to thicken, melt cheese in. Pour over cooked pasta.",
        "time": "25 mins", "one_pot": True
    },
    {
        "name": "Mushroom Risotto 🍄",
        "ingredients": {"rice", "mushrooms", "broth", "butter", "parmesan", "onion"},
        "instructions": "Sauté onions/mushrooms. Toast rice. Add broth ladle by ladle, stirring constantly.",
        "time": "40 mins", "one_pot": True
    },
    {
        "name": "Quesadillas 🧀",
        "ingredients": {"tortilla", "cheese", "chicken", "onion", "salsa"},
        "instructions": "Place cheese and chicken on tortilla, fold, fry in pan until crispy.",
        "time": "15 mins", "one_pot": True
    },
    {
        "name": "Mashed Potatoes & Chicken 🍗",
        "ingredients": {"potatoes", "butter", "milk", "chicken", "salt"},
        "instructions": "Boil and mash potatoes with butter/milk. Serve with roasted chicken.",
        "time": "45 mins", "one_pot": False
    },
    {
        "name": "Chicken Noodle Soup 🍜",
        "ingredients": {"chicken", "broth", "carrots", "celery", "pasta", "onion"},
        "instructions": "Sauté veggies. Add broth and chicken. Simmer. Add pasta near the end.",
        "time": "40 mins", "one_pot": True
    },
    {
        "name": "Baked Salmon 🐟",
        "ingredients": {"salmon", "lemon", "butter", "garlic", "herbs"},
        "instructions": "Place salmon on foil. Top with butter, garlic, lemon. Bake 400F for 12-15 mins.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "Stuffed Bell Peppers 🫑",
        "ingredients": {"bell pepper", "ground beef", "rice", "cheese", "tomato sauce"},
        "instructions": "Hollow out peppers. Fill with cooked beef/rice/sauce mix. Top with cheese. Bake 375F for 30m.",
        "time": "45 mins", "one_pot": True
    },
    {
        "name": "Veggie Fajitas 🌮",
        "ingredients": {"bell pepper", "onion", "tortilla", "lime", "oil", "chili powder"},
        "instructions": "Slice peppers and onions. Fry in hot oil with spices. Serve in warm tortillas with lime.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "Ratatouille 🍆",
        "ingredients": {"zucchini", "eggplant", "bell pepper", "tomato", "onion", "olive oil"},
        "instructions": "Slice all veggies into rounds. Layer in a baking dish with oil and herbs. Bake until tender.",
        "time": "50 mins", "one_pot": True
    },
    {
        "name": "Eggplant Parmesan 🍆",
        "ingredients": {"eggplant", "tomato sauce", "cheese", "flour", "oil", "parmesan"},
        "instructions": "Bread and fry eggplant slices. Layer with sauce and cheeses in dish. Bake until bubbly.",
        "time": "50 mins", "one_pot": True
    },
    {
        "name": "Roasted Cauliflower Tacos 🌮",
        "ingredients": {"cauliflower", "tortilla", "lime", "cabbage", "avocado", "oil"},
        "instructions": "Roast cauliflower florets with spices. Serve in tacos with cabbage slaw and avocado.",
        "time": "30 mins", "one_pot": True
    },
    {
        "name": "Banana Bread 🍌",
        "ingredients": {"banana", "flour", "sugar", "butter", "eggs"},
        "instructions": "Mash bananas, mix with wet then dry ingredients. Bake 350F for 60 mins.",
        "time": "70 mins", "one_pot": True
    },
    {
        "name": "Choc Chip Cookies 🍪",
        "ingredients": {"flour", "sugar", "butter", "chocolate chips", "eggs", "baking powder"},
        "instructions": "Cream butter/sugar, add eggs, mix in dry ingredients and chocolate. Bake 350F for 10m.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "Chocolate Mug Cake ☕",
        "ingredients": {"flour", "sugar", "cocoa powder", "milk", "oil", "chocolate chips"},
        "instructions": "Mix all ingredients in a microwave-safe mug. Microwave for 60-90 seconds.",
        "time": "5 mins", "one_pot": True
    },
    {
        "name": "Guacamole & Chips 🥑",
        "ingredients": {"avocado", "onion", "tomato", "lime", "tortilla chips"},
        "instructions": "Mash avocado with lime and salt. Stir in diced onion/tomato. Serve with chips.",
        "time": "10 mins", "one_pot": False
    },
    {
        "name": "Apple Slices & Peanut Butter 🍎",
        "ingredients": {"apple", "peanut butter"},
        "instructions": "Slice apple, dip in peanut butter. Simple and healthy.",
        "time": "5 mins", "one_pot": False
    },
    {
        "name": "Deviled Eggs 🥚",
        "ingredients": {"eggs", "mayo", "mustard", "paprika"},
        "instructions": "Boil eggs, peel, halve. Mix yolks with mayo/mustard. Pipe back in. Dust paprika.",
        "time": "20 mins", "one_pot": True
    },
    {
        "name": "Sweet Potato Fries 🍟",
        "ingredients": {"sweet potato", "oil", "salt", "paprika", "cornstarch"},
        "instructions": "Cut potatoes into sticks. Toss with cornstarch, oil, spices. Bake 425F until crispy (25m).",
        "time": "35 mins", "one_pot": True
    },
    {
        "name": "Roasted Asparagus 🌿",
        "ingredients": {"asparagus", "olive oil", "lemon", "parmesan", "garlic"},
        "instructions": "Toss asparagus in oil and garlic. Roast 400F for 10-15 mins. Top with lemon/parmesan.",
        "time": "20 mins", "one_pot": True
    }
]

# --- APP LOGIC ---

all_possible_ingredients = set()
for r in recipes:
    all_possible_ingredients.update(r['ingredients'])

sorted_ingredients = sorted(list(all_possible_ingredients))

# --- SIDEBAR ---
st.sidebar.write("What do you have?")
user_input_text = st.sidebar.text_area("Type items (e.g. eggs, onions, tofu):", "eggs, cheese, butter")

# PROCESS INPUT
raw_items = re.split(r'[,\n]', user_input_text)
cleaned_items = [x.strip().lower() for x in raw_items if x.strip()]

user_fridge = set()
recognized_items = []

for item in cleaned_items:
    if item in sorted_ingredients:
        user_fridge.add(item)
        recognized_items.append(item)
    else:
        for db_item in sorted_ingredients:
            if item in db_item or db_item in item: 
                if len(item) > 3 and (item in db_item or db_item in item):
                    user_fridge.add(db_item)
                    recognized_items.append(db_item)
                    break
                elif item == db_item[:-1]:
                    user_fridge.add(db_item)
                    recognized_items.append(db_item)
                    break

if recognized_items:
    st.sidebar.write("Found ingredients:")
    tags_html = "".join([f'<span class="sidebar-tag">{ing}</span>' for ing in set(recognized_items)])
    st.sidebar.markdown(tags_html, unsafe_allow_html=True)

st.sidebar.markdown("---")
only_full_match = st.sidebar.checkbox("✅ Cook Now (Full Match)", value=False)

# --- TABS ---
st.write(" ")
tab1, tab2, tab3, tab4 = st.tabs(["🍽 All Recipes", "🌱 Vegan", "🥘 One Pot", "🥕 Simple (5-6 Ingred)"])

def render_recipes(filter_mode="all"):
    matches = []
    
    for recipe in recipes:
        required_ingredients = recipe['ingredients']
        matching_items = user_fridge.intersection(required_ingredients)
        missing_items = required_ingredients - user_fridge
        match_percent = int((len(matching_items) / len(required_ingredients)) * 100)
        
        # GLOBAL FILTER
        if only_full_match and match_percent < 100:
            continue
            
        # TAB FILTERS
        if filter_mode == "vegan":
            if not required_ingredients.isdisjoint(NON_VEGAN_ITEMS):
                continue
        elif filter_mode == "simple":
            if not (5 <= len(required_ingredients) <= 6):
                continue
        elif filter_mode == "one_pot":
            if not recipe.get("one_pot", False):
                continue
        
        if len(matching_items) >= 1:
            matches.append({
                "recipe": recipe,
                "matching_items": matching_items,
                "missing_items": missing_items,
                "match_percent": match_percent
            })
            
    matches.sort(key=lambda x: x['match_percent'], reverse=True)
    
    if not matches:
        st.info("No recipes found in this category with your current ingredients!")
        return

    col1, col2 = st.columns(2)
    for i, item in enumerate(matches):
        recipe = item['recipe']
        ing_count = len(recipe['ingredients'])
        
        with (col1 if i % 2 == 0 else col2):
            with st.container(border=True):
                st.subheader(recipe['name'])
                st.markdown(f'<span class="recipe-time">⏱️ {recipe.get("time", "--")}</span>', unsafe_allow_html=True)
                
                if item['match_percent'] == 100:
                    st.progress(item['match_percent'], text="🔥 Perfect Match!")
                else:
                    st.progress(item['match_percent'], text=f"{item['match_percent']}% Match")
                
                st.write("**You have:**")
                have_html = "".join([f'<span class="have-tag">✔ {ing}</span>' for ing in item['matching_items']])
                st.markdown(have_html, unsafe_allow_html=True)
                
                if item['missing_items'] and not only_full_match:
                    st.write("**You need:**")
                    missing_html = "".join([f'<span class="missing-tag">{ing}</span>' for ing in item['missing_items']])
                    st.markdown(missing_html, unsafe_allow_html=True)
                
                if item['match_percent'] == 100:
                     st.success("✅ Ready to cook!")

                with st.expander("📝 View Instructions"):
                    st.write(recipe['instructions'])

# Render content
with tab1: render_recipes("all")
with tab2: render_recipes("vegan")
with tab3: render_recipes("one_pot")
with tab4: render_recipes("simple")
