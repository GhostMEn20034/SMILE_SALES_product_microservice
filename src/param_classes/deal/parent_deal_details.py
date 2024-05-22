from bson import ObjectId


class ParentDealDetailsParams:
    def __init__(self, deal_id: ObjectId, collection_name: str):
        self.deal_id: ObjectId = deal_id
        self.collection_name: str = collection_name
