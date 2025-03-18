import re
import secrets
import string
import streamlit as st
import streamlit.components.v1 as components
from typing import Tuple, List

# ------------------------------------------------------------------------------
# Constants and Helper Functions
# ------------------------------------------------------------------------------

# A set of common (blacklisted) passwords
BLACKLIST = frozenset({
    "password", "password123", "123456", "qwerty", "letmein",
    "admin", "welcome", "111111", "123123", "iloveyou", "master",
    "sunshine", "123456789", "football", "baseball", "monkey",
    "letmein", "shadow", "password1", "12345678", "1234", "abc123",
    "1234567", "password!", "12345", "dragon", "qwerty123", "superman",
    "987654321", "mypass", "trustno1", "hello", "freedom", "princess",
    "qazwsx", "ninja", "azerty", "password12", "654321", "passw0rd",
    "qwertyuiop", "123321", "1234567890", "123456a", "letmein123", "666666",
    "123abc", "password1234", "qwerty1234", "123456789a", "123456789z", "123456789x"
})

def evaluate_password(password: str) -> Tuple[str, int, List[str]]:
    """
    Evaluate the strength of a given password using several metrics.

    Advanced metrics include:
        - Length-based scoring.
        - Presence of both uppercase and lowercase letters.
        - Inclusion of digits.
        - Inclusion of special characters from !@#$%^&*.
        - Bonus for very long passwords (16+ characters).
        - Warnings for characters repeated three times consecutively.
        - **Advanced:** Warnings for sequential (ascending or descending) characters
          (e.g., 'abc', '123', 'cba', '321').

    Args:
        password (str): The password to evaluate.

    Returns:
        Tuple[str, int, List[str]]:
            - strength (str): "Strong", "Moderate", or "Weak"
            - score (int): Total score (maximum of 6, with bonus points)
            - feedback (List[str]): Suggestions and warnings for improving the password.
    """
    score = 0
    feedback = []

    # Check against common blacklisted passwords.
    if password.lower() in BLACKLIST:
        feedback.append("This password is too common. Please choose a different one.")
        return "Weak", score, feedback

    # Length evaluation: +2 points if >=12, +1 if >=8; else prompt for more length.
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Increase the length to at least 8 characters.")

    # Ensure both uppercase and lowercase letters are used.
    if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Use both uppercase and lowercase letters.")

    # Check for digit presence.
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Include at least one numeric digit (0-9).")

    # Check for at least one special character among !@#$%^&*.
    if re.search(r'[!@#$%^&*]', password):
        score += 1
    else:
        feedback.append("Add at least one special character (!@#$%^&*).")

    # Bonus: Extra point for very long passwords (16 or more characters).
    if len(password) >= 16:
        score += 1

    # Check for repeated characters (3 or more times consecutively).
    if re.search(r'(.)\1\1', password):
        feedback.append("Avoid using the same character three times consecutively.")

    # Advanced metric: Check for sequential (ascending or descending) patterns.
    # This loop checks for both alphabetical and numerical sequences.
    for i in range(len(password) - 2):
        seg = password[i:i+3]
        if seg.isalpha() or seg.isdigit():
            # Ascending or descending sequence check.
            if (ord(seg[1]) == ord(seg[0]) + 1 and ord(seg[2]) == ord(seg[1]) + 1) or \
               (ord(seg[1]) == ord(seg[0]) - 1 and ord(seg[2]) == ord(seg[1]) - 1):
                feedback.append("Avoid using sequential characters (e.g., 'abc', 'cba', '123', or '321'); they weaken your password.")
                break

    # Final strength interpretation based on total score.
    if score >= 5:
        strength = "Strong"
    elif score >= 3:
        strength = "Moderate"
    else:
        strength = "Weak"

    return strength, score, feedback

def generate_strong_password(length: int = 12) -> str:
    """
    Generate a strong password that guarantees the inclusion of at least:
        - One uppercase letter.
        - One lowercase letter.
        - One digit.
        - One special character from !@#$%^&*.

    A minimum length of 8 characters is enforced.

    Args:
        length (int): Desired length of the password.

    Returns:
        str: A securely generated random password.
    """
    if length < 8:
        length = 8  # Enforce a minimum length

    # Guarantee inclusion of required character categories.
    password_chars = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*")
    ]
    
    allowed_chars = string.ascii_letters + string.digits + "!@#$%^&*"
    while len(password_chars) < length:
        password_chars.append(secrets.choice(allowed_chars))
    
    # Shuffle to randomize character positions.
    secrets.SystemRandom().shuffle(password_chars)
    generated = "".join(password_chars)
    
    # Extra safety: If generated password is accidentally blacklisted, regenerate.
    if generated.lower() in BLACKLIST:
        return generate_strong_password(length)
    
    return generated

# ------------------------------------------------------------------------------
# Streamlit Application Interface with Theming, Functionality, and Feedback Panel
# ------------------------------------------------------------------------------

# Sidebar: Theme Selector
theme = st.sidebar.radio("Select Theme", ("Light Mode", "Dark Mode"))

# Apply custom CSS using robust selectors for the app and sidebar.
if theme == "Dark Mode":
    st.markdown(
        """
        <style>
        [data-testid="stApp"] {
            background-color: #212121;
            color: #e0e0e0;
        }
        [data-testid="stSidebar"] {
            background-color: #2c2c2c;
            color: #e0e0e0;
        }
        .stTextInput>div>input {
            background-color: #333333;
            color: #e0e0e0;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        [data-testid="stApp"] {
            background-color: #ffffff;
            color: #000000;
        }
        [data-testid="stSidebar"] {
            background-color: #f5f5f5;
            color: #000000;
        }
        .stTextInput>div>input {
            background-color: #ffffff;
            color: #000000;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------------------
# Main Content
# ------------------------------------------------------------------------------
st.title("🔒 Password Strength Meter & Generator")
st.markdown("This interactive tool evaluates the strength of your password and generates a strong alternative to improve your online security.")

# --- Password Evaluation Section ---
st.subheader("Evaluate Your Password")
with st.form(key="password_evaluation_form"):
    user_password = st.text_input("Enter your password:", type="password")
    evaluate_submitted = st.form_submit_button("Evaluate Password")

if evaluate_submitted:
    if user_password:
        strength, score, suggestions = evaluate_password(user_password)
        st.markdown(f"**Strength:** {strength} (Score: {score}/6)")
        if suggestions:
            st.markdown("**Suggestions for Improvement:**")
            for suggestion in suggestions:
                st.markdown(f"- {suggestion}")
    else:
        st.error("Please enter a password to evaluate.")

st.markdown("---")

# --- Password Generator Section ---
st.subheader("Generate a Strong Password")
password_length = st.slider("Select desired password length:", min_value=8, max_value=32, value=12, step=1)

if st.button("Generate Password"):
    new_password = generate_strong_password(password_length)
    st.markdown("**Suggested Strong Password:**")
    st.code(new_password, language="text")
    
    # Clipboard integration: Embed a button using HTML and JavaScript to copy the password.
    components.html(
        f"""
        <html>
          <head>
            <script>
              function copyToClipboard() {{
                navigator.clipboard.writeText("{new_password}");
                alert("Password copied to clipboard!");
              }}
            </script>
          </head>
          <body>
            <button onclick="copyToClipboard()" 
                    style="background-color: #4CAF50; color: white; border: none; padding: 10px 15px; 
                           border-radius: 5px; cursor: pointer;">
              Copy to Clipboard
            </button>
          </body>
        </html>
        """,
        height=100
    )

st.markdown("---")

# --- User Feedback Panel ---
st.subheader("Your Feedback")
with st.form(key="feedback_form"):
    st.markdown("**We'd love to hear your thoughts on this tool!**")
    rating: int = st.slider("How do you rate this tool? (1 = Poor, 5 = Excellent)", 
                             min_value=1, max_value=5, value=3, step=1)
    feedback_text: str = st.text_area("Enter any comments or suggestions:", placeholder="Your feedback...")
    feedback_submitted = st.form_submit_button("Submit Feedback")

if feedback_submitted:
    if feedback_text.strip():
        st.success("Thank you for your valuable feedback!")
    else:
        st.info("Thank you for your rating!")

# ------------------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------------------
st.markdown("---")
st.markdown("Made with ❤️ by SYED ZEESHAN IQBAL")
