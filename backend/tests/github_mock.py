from unittest.mock import patch

@patch('utils.github_helpers.github_user_exists')
def test_create_team_with_mocked_github(mock_github, client, auth_headers, create_users, create_project):
    mock_github.return_value = True  # Mock the GitHub user existence check

    payload = {
        "team_name": "Delta Team",
        "github_repo_url": "https://github.com/example/delta",
        "emails": [user.email for user in create_users]
    }

    response = client.post(
        "/api/teams",
        data=json.dumps(payload),
        headers=auth_headers
    )

    assert response.status_code == 201
    # Additional assertions...