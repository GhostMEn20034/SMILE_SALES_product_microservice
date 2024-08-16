from httpx import AsyncClient
from pytest_mock import MockerFixture

from testing_utils.search_terms.search_repository_return_values import (
    matched_search_terms, the_most_popular_search_terms
)

class TestSearchTermsInput:
    async def test_finding_search_terms_by_name_should_pass(self, mocker: MockerFixture, async_client: AsyncClient):
        mocked_found_search_terms = mocker.patch(
            'src.repositories.search_term.SearchTermRepository.find_search_terms_by_name',
            return_value=matched_search_terms(),
        )
        mocked_popular_search_terms = mocker.patch(
            'src.repositories.search_term.SearchTermRepository.get_the_most_popular_search_terms',
            return_value=the_most_popular_search_terms(),
        )

        response = await async_client.get("/api/v1/search/", params={"q": "De"})

        assert response.status_code == 200

        search_terms = response.json()
        assert all(term.get("trend_search_term") == False for term in search_terms), \
            "Not all items have 'trend_search_term': False"

        assert mocked_found_search_terms.called == True
        assert mocked_popular_search_terms.called == False

    async def test_empty_name_should_return_popular_terms(self, mocker: MockerFixture, async_client: AsyncClient):
        mocked_found_search_terms = mocker.patch(
            'src.repositories.search_term.SearchTermRepository.find_search_terms_by_name',
            return_value=matched_search_terms(),
        )
        mocked_popular_search_terms = mocker.patch(
            'src.repositories.search_term.SearchTermRepository.get_the_most_popular_search_terms',
            return_value=the_most_popular_search_terms(),
        )
        response = await async_client.get("/api/v1/search/")

        assert response.status_code == 200

        search_terms = response.json()
        assert all(term.get("trend_search_term") == True for term in search_terms), \
            "Not all items have 'trend_search_term': True"

        assert mocked_found_search_terms.called == False
        assert mocked_popular_search_terms.called == True
