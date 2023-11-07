# Social Media App

This is a social media application developed using Flask and SQLAlchemy.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Routes](#routes)
- [Contributing](#contributing)
- [License](#license)

## Description

The Social Media App allows users to create an account, log in, post content, follow other users, and view their posts. Users can update their profile information and search for other users. The application uses a SQLite database to store user information, posts, and follower relationships.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/KisalayGhosh/BLOGLITE.git
   ```

2. Change into the project directory:

   ```bash
   cd social-media-app
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Initialize the database:

   ```bash
   flask db init
   ```

6. Run the application:

   ```bash
   flask run
   ```

7. Open a web browser and navigate to `http://localhost:5000` to access the application.

## Usage

1. Register an account by providing the required information.
2. Log in with your username and password.
3. Create posts by clicking on the "New Post" button.
4. View your own profile and update your information if needed.
5. Search for other users by entering a username, first name, or last name in the search bar.
6. Follow and unfollow other users to see their posts on your home feed.
7. View other users' profiles to see their posts and follower information.
8. Update or delete your own posts from your profile page.

## Routes

- `/`: The login page. Users can log in with their credentials.
- `/registration`: The registration page. New users can create an account.
- `/<username>/home`: The home page for a logged-in user. Displays posts from followed users.
- `/<username>/my_profile`: The user's own profile page. Displays profile information and posts.
- `/<username>/update`: Update the user's profile information.
- `/<username>/search`: Search for other users.
- `/<username>/new_post`: Create a new post.
- `/<username>/profile/<other_username>`: View the profile of another user.
- `/<username>/delete/<post_id>`: Delete a post.
- `/<username>/update/<post_id>`: Update a post.
- `/<follower>/follow/<following>`: Follow a user.
- `/<follower>/unfollow/<following>`: Unfollow a user.

## Contributing

Contributions to the Social Media App are welcome! If you find a bug or have a suggestion for improvement, please open an issue or submit a pull request.

## Project video
[Link](https://drive.google.com/file/d/1BFV8rztExHF5mWE-dYOsBQ8mxSBJGaUU/view?usp=sharing)

## License

This project is licensed under the [MIT License](LICENSE).
