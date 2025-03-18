# Password Strength Meter & Generator

A Streamlit-based application that evaluates the strength of your password and generates a strong, secure password. This tool not only checks for basic password criteria but also includes advanced evaluation metrics—such as detecting sequential patterns and repeated characters—and features a clipboard integration for easy copying of generated passwords.

## Features

- **Password Strength Evaluation**
  - Checks for common weak passwords (blacklist).
  - Evaluates multiple criteria: length, use of uppercase & lowercase letters, inclusion of digits and special characters.
  - Advanced metrics: warns against sequential characters (e.g., `abc`, `123`) and repeated sequences.
- **Password Generation**
  - Generates a password that includes at least one uppercase letter, one lowercase letter, one digit, and one special character.
  - Enforces a user-selectable length (minimum of 8 characters).
- **Clipboard Integration**
  - An integrated button allows you to quickly copy the generated password to your clipboard.
- **User Feedback Panel**
  - Users can rate and provide feedback on the tool through a dedicated feedback form.
- **Theme Selector**
  - Choose between Light Mode and Dark Mode to customize the app’s appearance.

## Advanced Evaluation Metrics

- **Blacklist Check:** Rejects commonly used passwords.
- **Sequential Pattern Detection:** Identifies ascending or descending sequences.
- **Repeated Characters Warning:** Detects characters repeated three or more times in succession.

## Prerequisites

- Python 3.7 or higher
- [Streamlit](https://streamlit.io/) library

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your_username/password-strength-meter.git
   cd password-strength-meter
