import streamlit as st

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
    # SIMPLE RECIPE LOGIC
    # -----------------------------

    recipe = ""

    if "chicken" in prompt.lower():

        recipe = """
🍗 **Yogurt Chicken Skillet**

**FAST (20 min)**  
Pan-seared chicken with creamy yogurt sauce and sautéed spinach.

**BALANCED (40 min)**  
Creamy spinach chicken served over rice.

**PROJECT (1 hr)**  
Baked yogurt chicken casserole.

💡 **Waste Prevention Tip**  
Spinach wilting soon? Freeze it for smoothies or soups.

💰 Estimated Savings: **$8**  
🌍 Impact: **1.2kg CO₂ prevented**
"""

    elif "egg" in prompt.lower():

        recipe = """
🍳 **Cheesy Breakfast Toast**

**FAST**  
Toast bread, fry eggs, melt cheese on top.

**BALANCED**  
Omelette sandwich with toasted bread.

**PROJECT**  
Savory breakfast casserole.

💡 **Waste Prevention Tip**  
Bread getting stale? Turn it into breadcrumbs.
"""

    elif "rice" in prompt.lower():

        recipe = """
🍚 **Vegetable Fried Rice**

1. Heat oil in a pan  
2. Add carrots and garlic  
3. Stir in rice and soy sauce  
4. Cook until golden

Optional Add-ins:
• Egg
• Chicken
• Tofu

💡 **Waste Prevention Tip**
Cooked rice lasts 3–4 days in the fridge.
"""

    else:

        recipe = """
🥗 **Pantry Idea**

Try mixing your ingredients into:

**FAST:** Simple stir fry  
**BALANCED:** Pasta or rice bowl  
**PROJECT:** Baked casserole

💡 Tip: Use expiring ingredients first!
"""

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