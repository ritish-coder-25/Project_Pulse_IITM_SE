import pytest
import json
import os
from datetime import datetime, timedelta
from unittest.mock import patch, mock_open

# Test data
MOCK_COMMITS_RESPONSE = {
    "ishdeep": {
        "total_commits": 2,
        "commit_details": [
            {
                "sha": "abc123",
                "message": "Test commit",
                "date": "2024-03-20T10:00:00Z"
            }
        ]
    }
}

MOCK_FILE_CONTENT = {
    "user1": {
        "commit_details": [{
            "file_changes": [{
                "code_changes": "def test(): pass"
            }]
        }]
    }
}

class TestGetAllCommitsResource:
    @pytest.fixture
    def mock_get_commits(self):
        with patch('apis.Ta_dashboard.commits_github.get_commits_with_changes_files') as mock:
            mock.return_value = MOCK_COMMITS_RESPONSE
            yield mock

    def test_get_commits_success(self, client, auth_headers, mock_get_commits):
        # Arrange
        params = {
            'since': (datetime.now() - timedelta(days=7)).isoformat(),
            'until': datetime.now().isoformat(),
            'repo_owner': 'ritish-coder-25',
            'repo_name': 'Project_Pulse_IITM_SE',
            'team_id': 1
        }
        
        # Act
        response = client.get(
            '/api/commits-fetch',
            query_string=params,
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'users' in data
        assert data['users'] == MOCK_COMMITS_RESPONSE

    def test_get_commits_no_data(self, client, auth_headers, mock_get_commits):
        # Arrange
        mock_get_commits.return_value = None
        params = {
            'since': datetime.now().isoformat(),
            'until': datetime.now().isoformat(),
            'repo_owner': 'test-owner',
            'repo_name': 'test-repo',
            'team_id': 1
        }
        
        # Act
        response = client.get(
            '/api/commits-fetch',
            query_string=params,
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['errorCode'] == 'no_commits_found'

class TestGenAICommitAnalysis:
    @pytest.fixture
    def mock_summarizer(self):
        with patch('apis.Ta_dashboard.commits_github.summarize_code_changes') as mock:
            mock.return_value = {"summary": "Test summary"}
            yield mock

    def test_genai_analysis_success(self, client, auth_headers, mock_summarizer, tmp_path):
        # Arrange
        test_file = tmp_path / "test_changes.json"
        test_file.write_text(json.dumps(MOCK_FILE_CONTENT))
        
        request_data = {
            "file_path": str(test_file),
            "team_id": 1
        }
        
        # Act
        response = client.post(
            '/api/genai-commits-analysis',
            json=request_data,
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'summary' in data
        assert 'saved_to' in data

    def test_genai_analysis_file_not_found(self, client, auth_headers):
        # Arrange
        request_data = {
            "file_path": "nonexistent_file.json"
        }
        
        # Act
        response = client.post(
            '/api/genai-commits-analysis/1',
            json=request_data,
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['errorCode'] == 'file_not_found'

    def test_genai_analysis_empty_file(self, client, auth_headers, tmp_path):
        # Arrange
        test_file = tmp_path / "empty_changes.json"
        test_file.write_text(json.dumps({}))
        
        request_data = {
            "file_path": str(test_file)
        }
        
        # Act
        response = client.post(
            '/api/genai-commits-analysis/1',
            json=request_data,
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['errorCode'] == 'empty_file' 