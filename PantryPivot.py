import streamlit as st
import google.genai as genai
import os

# Get Gemini API key from secrets, environment, or fallback
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.sidebar.error("Gemini API key not found. Please set it in secrets.toml or environment variable.")
    st.stop()

client = genai.Client(api_key=api_key)

st.set_page_config(
    page_title="PantryPivot",
    page_icon="🥗",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------

st.title("🥗 PantryPivot")
st.subheader("Turn What's Left Into What's Next")

st.markdown("---")

# -----------------------------
# SIDEBAR PANTRY INVENTORY
# -----------------------------

st.sidebar.header("🧺 Your Pantry")

ingredients = st.sidebar.multiselect(
    "Select ingredients you have:",
    [
        "Chicken",
        "Eggs",
        "Rice",
        "Spinach",
        "Bread",
        "Cheese",
        "Carrots",
        "Yogurt",
        "Tomatoes",
        "Onions",
        "Garlic"
    ]
)

st.sidebar.markdown("---")

# -----------------------------
# RECIPE PIVOT ENGINE CONTROLS
# -----------------------------

st.sidebar.header("🔄 Recipe Pivot Engine")

mode = st.sidebar.radio(
    "Mode:",
    ["Strict Mode", "Flexible Mode"],
    help="Strict: Use ONLY available ingredients. Flexible: Up to 2 additional staples."
)

cuisine_pivot = st.sidebar.text_input(
    "Cuisine Pivot (optional):",
    placeholder="e.g., Make this Mexican"
)

meal_type_pivot = st.sidebar.selectbox(
    "Meal Type Pivot:",
    ["None", "Breakfast", "Lunch", "Dinner", "Snack"],
    help="Transform into this meal type"
)

difficulty = st.sidebar.selectbox(
    "Difficulty Scaling:",
    ["Quick (15 min)", "Balanced (30-45 min)", "Weekend Project (1+ hr)"]
)

st.sidebar.markdown("---")

st.sidebar.header("📊 Impact Stats")

st.sidebar.metric("Money Saved", "$24")
st.sidebar.metric("Meals Rescued", "6")
st.sidebar.metric("CO₂ Prevented", "3.2kg")

# -----------------------------
# MAIN CHAT AREA
# -----------------------------

st.header("💬 Pantry Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
prompt = st.chat_input("Ask PantryPivot for a recipe...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    # -----------------------------
    # AI RECIPE GENERATION
    # -----------------------------

    # Build the AI prompt
        available_ingredients = ", ".join(ingredients) if ingredients else "none specified"

        system_prompt = f"""
You are PantryPivot, a helpful AI that creates recipes from available ingredients.

Available ingredients: {available_ingredients}

Mode: {mode}
- Strict Mode: Use ONLY the available ingredients listed above. No additional ingredients.
- Flexible Mode: Can suggest up to 2 additional basic staples (salt, pepper, oil, etc.).

Cuisine Pivot: {cuisine_pivot if cuisine_pivot else "None"}

Meal Type Pivot: {meal_type_pivot if meal_type_pivot != "None" else "None"}

Difficulty: {difficulty}

User request: {prompt}

Generate a recipe that fits the criteria. Include:
- Recipe name
- Prep/cook time
- Ingredients list (marking any additional staples)
- Step-by-step instructions
- Waste prevention tip
- Estimated savings and environmental impact
"""

        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=system_prompt + "\n\n" + prompt
            )
            recipe = response.text
        except Exception as e:
            recipe = f"Error generating recipe: {str(e)}"

    with st.chat_message("assistant"):
        st.write(recipe)

    st.session_state.messages.append(
        {"role": "assistant", "content": recipe}
    )

# -----------------------------
# QUICK ACTION BUTTONS
# -----------------------------

st.markdown("---")
st.subheader("⚡ Quick Recipe Ideas")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🥗 Salad Ideas"):
        st.success("Try a spinach, tomato, and cheese salad!")

with col2:
    if st.button("🍝 Pasta Night"):
        st.success("Creamy garlic pasta with spinach.")

with col3:
    if st.button("🍳 Breakfast for Dinner"):
        st.success("Egg fried rice or omelette toast!")