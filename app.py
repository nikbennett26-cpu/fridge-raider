import streamlit as st
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Fridge Raider Pro",
    page_icon="🧊",
    layout="wide"
)

# --- 2. THE VISUAL ENGINE (CSS) ---
st.markdown("""
    <style>
    /* 1. BACKGROUND: The Deep Mesh Gradient */
    .stApp {
        background-color: #0f172a;
        background-image: 
            radial-gradient(at 0% 0%, #4c1d95 0px, transparent 50%),
            radial-gradient(at 100% 100%, #be185d 0px, transparent 50%),
            radial-gradient(at 50% 50%, #1e40af 0px, transparent 50%);
        background-size: 100% 100%;
        background-attachment: fixed;
    }

    /* 2. TEXT: Make everything White & Readable */
    h1, h2, h3, p, span, div, label {
        color: white !important;
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* 3. SIDEBAR: Frosted Glass Effect */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* 4. CARDS: The "Recipe" Containers */
    div.stExpander {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* 5. BUTTONS: Make them POP (White vs Purple) */
    .stButton > button {
        background-color: white !important;
        color: #4c1d95 !important; /* Purple Text */
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
        transition: transform 0.1s ease-in-out;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
    }

    /* 6. METRICS: Gold Colors for Stats */
    div[data-testid="stMetricValue"] {
        color: #fbbf24 !important; /* Amber-400 */
        font-size: 2.5rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. GAMIFICATION STATE ---
if 'streak' not in st.session_state:
    st.session_state.streak = 3
if 'xp' not in st.session_state:
    st.session_state.xp = 150

def cook_action():
    st.session_state.streak += 1
    st.session_state.xp += 50
    st.balloons()
    st.toast("🔥 Delicious! +50 XP Earned!")

# --- 4. RECIPE DATA ---
recipes = [
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
        "name": "Avocado Toast 🥑",
        "ingredients": {"bread", "avocado", "salt", "lemon", "oil"},
        "instructions": "Toast bread, smash avocado on top, season with salt and lemon.",
        "image": "https://images.unsplash.com/photo-1588137372308-15f75323a557?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Grilled Cheese 🥪",
        "ingredients": {"bread", "cheese", "butter"},
        "instructions": "Butter bread, place cheese inside, grill until golden.",
        "image": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Fruit Smoothie 🥤",
        "ingredients": {"banana", "milk", "honey", "ice"},
        "instructions": "Blend all ingredients until smooth.",
        "image": "https://images.unsplash.com/photo-1505252585461-04db1eb84625?auto=format&fit=crop&w=400&q=80"
    },
    {
        "name": "Pasta Pomodoro 🍝",
        "ingredients": {"pasta", "tomato sauce", "garlic", "oil"},
        "instructions": "Boil pasta. Sauté garlic in oil, add sauce, mix with pasta.",
        "image": "https://images.unsplash.com/photo-1626844131082-256783844137?auto=format&fit=crop&w=400&q=80"
    }
]

# --- 5. SIDEBAR (THE FRIDGE) ---
st.sidebar.title("🧊 Fridge Raider")
st.sidebar.markdown("Select what you have in your kitchen:")

all_possible_ingredients = set()
for r in recipes:
    all_possible_ingredients.update(r['ingredients'])
sorted_ingredients = sorted(list(all_possible_ingredients))

user_ingredients = st.sidebar.multiselect(
    "Ingredients:", 
    options=sorted_ingredients,
    default=["eggs", "cheese", "butter", "bread"]
)
user_fridge = set(user_ingredients)

# --- 6. MAIN DASHBOARD ---
# Header Area
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    st.title("What's Cooking?")
    st.caption(f"We found recipes based on your **{len(user_fridge)} ingredients**.")
with col2:
    st.metric("🔥 Streak", f"{st.session_state.streak} Days")
with col3:
    st.metric("✨ XP", st.session_state.xp)

st.markdown("---")

# --- 7. RECIPE GRID LOGIC ---
found_match = False
cols = st.columns(3) # Create a 3-column grid layout

for i, recipe in enumerate(recipes):
    required_ingredients = recipe['ingredients']
    matching_items = user_fridge.intersection(required_ingredients)
    
    # Logic: Show if we have at least 1 matching ingredient
    if len(matching_items) >= 1:
        found_match = True
        missing = required_ingredients - user_fridge
        
        # Determine which column to place this card in (0, 1, or 2)
        with cols[i % 3]:
            # The "Card" UI
            with st.expander(f"{recipe['name']}", expanded=True):
                st.image(recipe['image'], use_container_width=True)
                
                # Match Percentage Bar
                match_percent = int((len(matching_items) / len(required_ingredients)) * 100)
                
                if not missing:
                    st.progress(100, "100% Match!")
                    st.success("You have everything!")
                    if st.button("I Cooked This", key=f"btn_{i}"):
                        cook_action()
                else:
                    st.progress(match_percent, f"{match_percent}% Match")
                    st.markdown(f"**Missing:** {', '.join(missing)}")
                    st.button("Add to Shopping List", key=f"shop_{i}")

if not found_match:
    st.warning("No matches found! Try adding more ingredients in the sidebar.")
