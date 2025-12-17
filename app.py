import streamlit as st

st.set_page_config(page_title="Fridge Raider v3 Pro", layout="wide")

# --- CSS: THE MESH GRADIENT BACKGROUND ---
st.markdown("""
<style>
    /* Target the main Streamlit container */
    .stApp {
        background-color: #ffdeeb;
        background-image: 
            radial-gradient(at 80% 0%, hsla(189,100%,56%,0.3) 0px, transparent 50%),
            radial-gradient(at 0% 50%, hsla(355,100%,93%,0.3) 0px, transparent 50%),
            radial-gradient(at 80% 50%, hsla(340,100%,76%,0.3) 0px, transparent 50%),
            radial-gradient(at 0% 100%, hsla(22,100%,77%,0.3) 0px, transparent 50%),
            radial-gradient(at 80% 100%, hsla(242,100%,70%,0.3) 0px, transparent 50%),
            radial-gradient(at 0% 0%, hsla(343,100%,76%,0.3) 0px, transparent 50%);
    }
    
    /* Make the cards slightly transparent white to pop against the background */
    div[data-testid="stExpander"], div[data-testid="stImage"] {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Enhance the title text */
    h1 {
        color: #1f2937;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.title("🧊 Fridge Raider v3 Pro")
st.write("Select the ingredients you have, and I'll tell you what to cook!")

# --- THE MASSIVE RECIPE DATABASE (45+ ITEMS) ---
recipes = [
    # --- BREAKFAST ---
    {
        "name": "Classic Omelette 🍳",
        "ingredients": {"eggs", "cheese", "butter", "salt"},
        "instructions": "Whisk eggs, melt butter, cook until fluffy, add cheese.",
        "image": "https://images.unsplash.com/photo-1510693206972-df098062cb71?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Fluffy Pancakes 🥞",
        "ingredients": {"eggs", "milk", "flour", "butter", "sugar"},
        "instructions": "Mix dry and wet ingredients separately, combine, and fry in butter.",
        "image": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "French Toast 🍞",
        "ingredients": {"bread", "eggs", "milk", "cinnamon", "butter"},
        "instructions": "Dip bread in egg/milk mix, fry in butter until golden brown.",
        "image": "https://images.unsplash.com/photo-1484723091739-30a097e8f929?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Oatmeal Bowl 🥣",
        "ingredients": {"oats", "milk", "honey", "banana", "cinnamon"},
        "instructions": "Cook oats in milk, top with sliced banana and honey.",
        "image": "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Yogurt Parfait 🍓",
        "ingredients": {"yogurt", "granola", "berries", "honey"},
        "instructions": "Layer yogurt, granola, and fresh berries. Drizzle with honey.",
        "image": "https://images.unsplash.com/photo-1488477181946-6428a029177b?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Fruit Smoothie 🥤",
        "ingredients": {"banana", "milk", "honey", "ice"},
        "instructions": "Blend all ingredients until smooth.",
        "image": "https://images.unsplash.com/photo-1505252585461-04db1eb84625?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Avocado Toast with Egg 🥑",
        "ingredients": {"bread", "avocado", "eggs", "chili flakes", "lemon"},
        "instructions": "Toast bread, smash avocado with lemon. Top with fried/poached egg and chili.",
        "image": "https://images.unsplash.com/photo-1525351484164-8035a4206501?auto=format&fit=crop&w=400&q=80"
    },

    # --- LUNCH ---
    {
        "name": "Grilled Cheese Sandwich 🥪",
        "ingredients": {"bread", "cheese", "butter"},
        "instructions": "Butter bread, place cheese inside, grill until golden.",
        "image": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "BLT Sandwich 🥓",
        "ingredients": {"bread", "bacon", "lettuce", "tomato", "mayo"},
        "instructions": "Cook bacon, toast bread, layer ingredients with mayo.",
        "image": "https://images.unsplash.com/photo-1553909489-cd47e3faaefc?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Classic Tuna Salad 🐟",
        "ingredients": {"tuna", "mayo", "onion", "celery", "bread"},
        "instructions": "Mix tuna, mayo, diced onion and celery. Serve on bread or lettuce.",
        "image": "https://images.unsplash.com/photo-1550505393-885efce5988d?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Caesar Salad 🥗",
        "ingredients": {"lettuce", "croutons", "parmesan", "chicken", "dressing"},
        "instructions": "Toss lettuce with dressing, top with grilled chicken and croutons.",
        "image": "https://images.unsplash.com/photo-1550304943-4f24f54ddde9?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Greek Salad 🇬🇷",
        "ingredients": {"cucumber", "tomato", "feta", "olives", "onion", "olive oil"},
        "instructions": "Chop veggies roughly. Toss with olive oil and top with block of feta.",
        "image": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Caprese Salad 🇮🇹",
        "ingredients": {"tomato", "mozzarella", "basil", "olive oil", "balsamic vinegar"},
        "instructions": "Slice tomatoes and cheese, arrange with basil, drizzle with oil.",
        "image": "https://images.unsplash.com/photo-1529312266912-b33cf6227e24?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Hummus & Veggies 🥕",
        "ingredients": {"chickpeas", "lemon", "garlic", "olive oil", "tahini", "carrots"},
        "instructions": "Blend chickpeas, lemon, garlic, tahini and oil. Serve with carrot sticks.",
        "image": "https://images.unsplash.com/photo-1577906096429-f736f6f3a35d?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Quinoa Salad 🥣",
        "ingredients": {"quinoa", "cucumber", "tomato", "lemon", "feta", "parsley"},
        "instructions": "Cook quinoa. Mix with chopped veggies, crumbled feta, lemon juice and herbs.",
        "image": "https://images.unsplash.com/photo-1623428187969-5da2dcea5ebf?auto=format&fit=crop&w=400&q=80"
    },

    # --- DINNER ---
    {
        "name": "Tomato Pasta 🍝",
        "ingredients": {"pasta", "tomato sauce", "garlic", "olive oil"},
        "instructions": "Boil pasta, sauté garlic in oil, add sauce, mix.",
        "image": "https://images.unsplash.com/photo-1626844131082-256783844137?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Pesto Pasta 🍃",
        "ingredients": {"pasta", "pesto", "parmesan", "cherry tomatoes"},
        "instructions": "Boil pasta. Save some pasta water. Toss pasta with pesto and a splash of water. Top with tomatoes.",
        "image": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Garlic Butter Shrimp 🍤",
        "ingredients": {"shrimp", "butter", "garlic", "lemon", "parsley"},
        "instructions": "Sauté garlic in butter. Add shrimp, cook 3 mins. Finish with lemon/parsley.",
        "image": "https://images.unsplash.com/photo-1559742811-822873691df8?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Chicken Stir Fry 🥡",
        "ingredients": {"chicken", "rice", "soy sauce", "vegetables", "oil"},
        "instructions": "Cook chicken, add veggies, stir in sauce, serve over rice.",
        "image": "https://images.unsplash.com/photo-1603133872878-684f10842619?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Tofu Stir Fry 🥦",
        "ingredients": {"tofu", "soy sauce", "ginger", "garlic", "broccoli", "rice"},
        "instructions": "Press tofu, cube, and fry. Remove. Fry aromatics and broccoli. Combine with sauce over rice.",
        "image": "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Beef & Broccoli 🥦",
        "ingredients": {"beef", "broccoli", "soy sauce", "garlic", "rice", "sugar"},
        "instructions": "Sear beef strips. Steam broccoli. Toss both in soy/garlic/sugar sauce. Serve over rice.",
        "image": "https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Spaghetti Carbonara 🇮🇹",
        "ingredients": {"pasta", "eggs", "cheese", "bacon", "black pepper"},
        "instructions": "Boil pasta. Fry bacon. Mix eggs and cheese. Toss hot pasta with egg mix (off heat).",
        "image": "https://images.unsplash.com/photo-1612874742237-6526221588e3?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Simple Tacos 🌮",
        "ingredients": {"tortilla", "ground beef", "cheese", "lettuce", "salsa"},
        "instructions": "Cook meat, fill tortillas, top with cheese and salsa.",
        "image": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Black Bean Burrito 🌯",
        "ingredients": {"tortilla", "black beans", "rice", "cheese", "salsa", "corn"},
        "instructions": "Warm beans and corn. Layer rice, beans, corn, and cheese in tortilla. Roll and serve.",
        "image": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Chicken Curry 🍛",
        "ingredients": {"chicken", "curry paste", "coconut milk", "rice", "onion"},
        "instructions": "Fry onion and chicken, add paste, pour in milk, simmer. Serve with rice.",
        "image": "https://images.unsplash.com/photo-1631292784640-2b24be784d5d?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Fried Rice 🍚",
        "ingredients": {"rice", "eggs", "soy sauce", "peas", "carrots", "oil"},
        "instructions": "Fry veggies, push to side, scramble eggs, add rice and sauce, mix high heat.",
        "image": "https://images.unsplash.com/photo-1603133872878-684f10842619?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Homemade Pizza 🍕",
        "ingredients": {"flour", "yeast", "tomato sauce", "cheese", "pepperoni"},
        "instructions": "Make dough, add sauce and toppings, bake at high heat (450F) for 12 mins.",
        "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Mac & Cheese 🧀",
        "ingredients": {"pasta", "cheese", "milk", "butter", "flour"},
        "instructions": "Make a roux with flour/butter, add milk to thicken, melt cheese in. Pour over cooked pasta.",
        "image": "https://images.unsplash.com/photo-1543339308-43e59d6b73a6?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Mushroom Risotto 🍄",
        "ingredients": {"rice", "mushrooms", "broth", "butter", "parmesan", "onion"},
        "instructions": "Sauté onions/mushrooms. Toast rice. Add broth ladle by ladle, stirring constantly.",
        "image": "https://images.unsplash.com/photo-1476124369491-e7addf5db371?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Quesadillas 🧀",
        "ingredients": {"tortilla", "cheese", "chicken", "onion", "salsa"},
        "instructions": "Place cheese and chicken on tortilla, fold, fry in pan until crispy.",
        "image": "https://images.unsplash.com/photo-1618040996337-56904b7850b9?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Mashed Potatoes & Chicken 🍗",
        "ingredients": {"potatoes", "butter", "milk", "chicken", "salt"},
        "instructions": "Boil and mash potatoes with butter/milk. Serve with roasted chicken.",
        "image": "https://images.unsplash.com/photo-1604908177453-7462950a6a3b?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Chicken Noodle Soup 🍜",
        "ingredients": {"chicken", "broth", "carrots", "celery", "pasta", "onion"},
        "instructions": "Sauté veggies. Add broth and chicken. Simmer. Add pasta near the end.",
        "image": "https://images.unsplash.com/photo-1547592166-23acbe346499?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Baked Salmon 🐟",
        "ingredients": {"salmon", "lemon", "butter", "garlic", "herbs"},
        "instructions": "Place salmon on foil. Top with butter, garlic, lemon. Bake 400F for 12-15 mins.",
        "image": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=400&q=80"
    },
    
    # --- DESSERT / SNACKS ---
    {
        "name": "Banana Bread 🍌",
        "ingredients": {"banana", "flour", "sugar", "butter", "eggs"},
        "instructions": "Mash bananas, mix with wet then dry ingredients. Bake 350F for 60 mins.",
        "image": "https://images.unsplash.com/photo-1596229961623-455b768172c7?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Choc Chip Cookies 🍪",
        "ingredients": {"flour", "sugar", "butter", "chocolate chips", "eggs", "baking powder"},
        "instructions": "Cream butter/sugar, add eggs, mix in dry ingredients and chocolate. Bake 350F for 10m.",
        "image": "https://images.unsplash.com/photo-1499636138143-bd630f5cf386?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Chocolate Mug Cake ☕",
        "ingredients": {"flour", "sugar", "cocoa powder", "milk", "oil", "chocolate chips"},
        "instructions": "Mix all ingredients in a microwave-safe mug. Microwave for 60-90 seconds.",
        "image": "https://images.unsplash.com/photo-1586985289906-406988974504?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Guacamole & Chips 🥑",
        "ingredients": {"avocado", "onion", "tomato", "lime", "tortilla chips"},
        "instructions": "Mash avocado with lime and salt. Stir in diced onion/tomato. Serve with chips.",
        "image": "https://images.unsplash.com/photo-1600850056064-a8b380aff831?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Apple Slices & Peanut Butter 🍎",
        "ingredients": {"apple", "peanut butter"},
        "instructions": "Slice apple, dip in peanut butter. Simple and healthy.",
        "image": "https://images.unsplash.com/photo-1632161845691-32c0211329c4?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Deviled Eggs 🥚",
        "ingredients": {"eggs", "mayo", "mustard", "paprika"},
        "instructions": "Boil eggs, peel, halve. Mix yolks with mayo/mustard. Pipe back in. Dust paprika.",
        "image": "https://images.unsplash.com/photo-1590412200988-a436970781fa?auto=format&fit=crop&w=400&q=80"
    }
]

# --- APP LOGIC ---

# 1. Setup ingredients list
all_possible_ingredients = set()
for r in recipes:
    all_possible_ingredients.update(r['ingredients'])

sorted_ingredients = sorted(list(all_possible_ingredients))

# 2. Sidebar Controls
st.sidebar.header("Your Fridge 🧊")
st.sidebar.write("What do you have today?")

user_ingredients = st.sidebar.multiselect(
    "Select ingredients:", 
    options=sorted_ingredients,
    default=["eggs", "cheese", "butter"]
)
user_fridge = set(user_ingredients)

# 3. Find and Display Matches
st.header("Recommended Recipes:")

# Filter matches first
matches = []
for recipe in recipes:
    required_ingredients = recipe['ingredients']
    matching_items = user_fridge.intersection(required_ingredients)
    
    if len(matching_items) >= 1:
        matches.append({
            "recipe": recipe,
            "matching_items": matching_items,
            "missing_items": required_ingredients - user_fridge,
            "match_percent": int((len(matching_items) / len(required_ingredients)) * 100)
        })

# Sort matches by percentage (highest match first)
matches.sort(key=lambda x: x['match_percent'], reverse=True)

if not matches:
    st.warning("No matches yet! Try selecting more ingredients from the sidebar.")
else:
    col1, col2 = st.columns(2)
    
    for i, item in enumerate(matches):
        recipe = item['recipe']
        
        # Display in alternating columns
        with (col1 if i % 2 == 0 else col2):
            st.image(recipe['image'], use_container_width=True)
            st.subheader(recipe['name'])
            
            # Progress bar for match strength
            st.progress(item['match_percent'], text=f"{item['match_percent']}% Match")
            
            if not item['missing_items']:
                st.success("✅ You have everything!")
            else:
                # Show what matches and what is missing
                st.write(f"**Have:** {', '.join(item['matching_items'])}")
                st.error(f"**Missing:** {', '.join(item['missing_items'])}")
                
            with st.expander("View Instructions"):
                st.write(recipe['instructions'])
            
            st.write("---")
