import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_retrieve_board(auth_client, goal, date_now, category, board_participant):
    url = reverse('retrieve_board', kwargs={'pk': goal.pk})
    response = auth_client.get(path=url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_list_board(auth_client, goal, date_now, category, board_participant):
    url = reverse('list_board')
    response = auth_client.get(path=url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_board(auth_client, board, test_user):
    url = reverse('create_board')
    payload = {
        'title': 'super title',
    }
    response = auth_client.post(
        path=url,
        data=payload
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data['title'] == payload['title']
