# social-game-rating

**Project Q** is a community-driven game rating platform designed to connect video game enthusiasts from around the world. Reminiscent of platforms like IMDB or Letterboxd, it allows users to rate, review, and discuss their favorite games.

The project is built with a scalable, API-first architecture, where the Django backend serves as a central data source for multiple clients, including the web interface and future native iOS and Android applications.

## Features

- **User Profiles**: Create and manage your own profile, showcasing your game preferences and reviews.
- **Game Ratings and Reviews**: Rate games, write reviews, and see what others think.
- **Custom Game Lists**: Organize and share your favorite games by creating personalized lists (e.g., "My Top 10 RPGs," "Games to Play in 2025").
- **Social Features**: Follow other users, see their activity, and engage through comments and likes.
- **Comprehensive Game Database**: Browse an extensive database of games with detailed information and community input.

## Tech Stack

The architecture is designed to be robust, scalable, and maintainable.

-   **Backend**: **Django (Python)**
    -   Provides a solid foundation for business logic, database management (ORM), and user authentication.
-   **API**: **Django REST Framework (DRF)**
    -   Used to create a comprehensive and secure RESTful API that exposes backend functionality to all clients.
-   **Web Frontend**: **HTML, CSS, JavaScript**
    -   Utilizes **Bootstrap** for a responsive, mobile-first design. The web app consumes the same API that the mobile apps will use.
-   **Database**: **PostgreSQL**
    -   A powerful, open-source object-relational database system known for reliability and data integrity.
-   **Deployment**: **Google Cloud Platform (GCP)** (Planned)
    -   For scalable hosting, database management, and infrastructure.

## Backend Architecture & API

This project follows an **API-first** design philosophy. The Django backend is not just for the website; it's a powerful, centralized server that provides data and services to any client through a well-defined RESTful API built with Django REST Framework.

This approach ensures that whether a user is on the website, an iOS app, or an Android app, they have a consistent experience and access to the same data and features. All core functionalities are exposed via API endpoints.

### Key API Resources

The API will provide endpoints for all major features, including but not limited to:

-   **Authentication**:
    -   `POST /api/auth/register/` - User registration.
    -   `POST /api/auth/login/` - Obtain authentication tokens (e.g., JWT).
    -   `POST /api/auth/logout/` - Invalidate tokens.
    -   `POST /api/auth/password/reset/` - Password reset functionality.

-   **Users & Profiles**:
    -   `GET /api/users/<username>/` - View user profiles.
    -   `PUT /api/users/me/` - Edit the authenticated user's profile.

-   **Social Interactions**:
    -   `POST /api/users/<username>/follow/` - Follow a user.
    -   `DELETE /api/users/<username>/follow/` - Unfollow a user.
    -   `GET /api/users/<username>/followers/` - List a user's followers.
    -   `GET /api/users/<username>/following/` - List users a user is following.

-   **Games & Ratings**:
    -   `GET /api/games/` - Search and browse games.
    -   `GET /api/games/<id>/` - Get details for a specific game.
    -   `POST /api/games/<id>/rate/` - Create or update a rating/review for a game.

-   **Game Lists**:
    -   `GET /api/lists/` - View lists created by the authenticated user.
    -   `POST /api/lists/` - Create a new game list.
    -   `GET /api/lists/<id>/` - View a specific list.
    -   `POST /api/lists/<id>/add_game/` - Add a game to a list.

By building out these endpoints, we ensure that when development begins on the iOS and Android apps, the backend will be ready to support them without requiring significant re-engineering.

## Getting Started (Local Development)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/social-game-rating.git
    cd social-game-rating
    ```
2.  **Set up the environment:**
    *(Instructions for setting up a virtual environment, installing dependencies from `requirements.txt`, and running migrations will be added here.)*

3.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
