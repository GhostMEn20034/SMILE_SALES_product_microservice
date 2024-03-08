from pymongo.results import InsertOneResult, InsertManyResult, UpdateResult, DeleteResult
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Optional, Dict, List


class BaseRepository:
    def __init__(self, db_instance: AsyncIOMotorDatabase, collection_name: str):
        self.db: AsyncIOMotorDatabase = db_instance
        self.collection_name: str = collection_name

    async def get_one_document(self, filters: Optional[Dict] = None, projection: Optional[Dict] = None,
                               **kwargs) -> Dict:
        """
        Returns a single document from the database based on the given filters.
        :param filters: A dictionary of filters to apply to the query.
        :param projection: A dictionary of fields which will be returned in result.
        :param kwargs: Any additional query parameters such as session etc.
        """
        if filters is None:
            filters = {}

        if projection is None:
            projection = {}

        document = await self.db[self.collection_name].find_one(filter=filters, projection=projection, **kwargs)
        return document

    async def get_document_list(self, filters: Optional[Dict] = None, projection: Optional[Dict] = None,
                                sort: Optional[Dict] = None, skip: int = 0, limit: int = 0, **kwargs) -> List[Dict]:
        """
        Returns a list of documents from the database based on the given filters.
        :param filters: A dictionary of filters to apply to the query.
        :param projection: A dictionary of fields which will be returned in result
        :param sort: A dictionary of fields by which the results will be sorted.
        :param skip: The number of documents to skip. (Also it's called OFFSET in Relational DBs)
        :param limit: The number of documents to return in result.
        :param kwargs: Any additional query parameters such as session etc.
        """
        if filters is None:
            filters = {}

        if projection is None:
            projection = {}

        if sort is None:
            sort = {}

        document_list = await self.db[self.collection_name] \
            .find(filters, projection, **kwargs).skip(skip).limit(limit).sort(sort).to_list(length=None)

        return document_list

    async def create_one_document(self, data_to_insert: Dict, **kwargs) -> InsertOneResult:
        """
        Creates a new document from the given data in dictionary.
        :param data_to_insert: A dictionary containing the data to be inserted
        :param kwargs: Any additional query parameters such as session etc.
        """
        created_document = await self.db[self.collection_name].insert_one(document=data_to_insert, **kwargs)
        return created_document

    async def create_many_documents(self, data_to_insert: List[Dict], **kwargs) -> InsertManyResult:
        """
        Creates a list of documents from the given data in List of dictionaries.
        :param data_to_insert: A list of dictionaries containing the data to be inserted.
        :param kwargs: Any additional query parameters such as session etc.
        """
        created_documents = await self.db[self.collection_name].insert_many(documents=data_to_insert, **kwargs)
        return created_documents

    async def update_one_document(self, filters: Optional[Dict] = None, data_to_update: Optional[Dict] = None,
                                  **kwargs) -> UpdateResult:
        """
        Updates a matched document by the data in dictionary.
        :param filters: Filters to match the document.
        :param data_to_update: A dictionary containing the data to update and operations on the data such as $set
        :param kwargs: Any additional query parameters such as session etc.
        """
        if filters is None:
            filters = {}

        if data_to_update is None:
            data_to_update = {}

        updated_document = await self.db[self.collection_name] \
            .update_one(filter=filters, update=data_to_update, **kwargs)

        return updated_document

    async def update_many_documents(self, filters: Optional[Dict] = None, data_to_update: Optional[Dict] = None,
                                    **kwargs) -> UpdateResult:
        """
        Updates a matched documents by the data in dictionary.
        :param filters: Filters to match documents.
        :param data_to_update: A dictionary containing the data to update and operations on the data such as $set
        :param kwargs: Any additional query parameters such as session etc.
        """
        if filters is None:
            filters = {}

        if data_to_update is None:
            data_to_update = {}

        updated_documents = await self.db[self.collection_name] \
            .update_many(filter=filters, update=data_to_update, **kwargs)

        return updated_documents

    async def delete_one_document(self, filters: Optional[Dict] = None, **kwargs) -> DeleteResult:
        """
        Deletes a matched document.
        :param filters: Filters to match the document.
        :param kwargs: Any additional query parameters such as session etc.
        """
        if filters is None:
            filters = {}

        deleted_document = await self.db[self.collection_name].delete_one(filter=filters, **kwargs)
        return deleted_document

    async def delete_many_documents(self, filters: Optional[Dict] = None, **kwargs) -> DeleteResult:
        """
        Deletes a matched documents.
        :param filters: Filters to match documents.
        :param kwargs: Any additional query parameters such as session etc.
        """
        if filters is None:
            filters = {}

        deleted_documents = await self.db[self.collection_name].delete_many(filter=filters, **kwargs)
        return deleted_documents

