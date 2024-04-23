from src.schemes.product.filters.product_list import ProductSortOptionsEnum


class SortStatementBuilder:
    """
    Responsible for building sort pipeline for products based on specified sort option
    """

    def __init__(self, sort_option: ProductSortOptionsEnum):
        self.sort_option = sort_option

    @staticmethod
    def build_price_sort_pipeline_stage(price_field_name="discounted_price", ascending: bool = True):
        """
        Returns pipeline stage for sorting products by price in ascending order if ascending is True,
        Otherwise it sorts products by price in descending order.
        """
        return {"$sort": {price_field_name: 1 if ascending else -1}}

    @staticmethod
    def build_stock_sort_pipeline_stage(stock_field_name="stock",ascending: bool = True):
        """
        Returns pipeline stage for sorting products by their stock in ascending order if ascending is True,
        Otherwise it sorts products by stock in descending order.
        Note that products that are out of stock (stock is 0) will always be last regardless of the sort order
        """
        return {"$sort": {"out_of_stock": 1, stock_field_name: 1 if ascending else -1}}

    def get_sort_pipeline_stage(self):
        """
        Returns pipeline for sorting based on sort option
        """
        if self.sort_option == ProductSortOptionsEnum.relevancy:
            sort_pipeline_stage = []
        elif self.sort_option == ProductSortOptionsEnum.price_low_to_high:
            sort_pipeline_stage = [
                self.build_price_sort_pipeline_stage()
            ]
        elif self.sort_option == ProductSortOptionsEnum.price_high_to_low:
            sort_pipeline_stage = [
                self.build_price_sort_pipeline_stage(ascending=False)
            ]
        elif self.sort_option == ProductSortOptionsEnum.ending_soonest:
            sort_pipeline_stage = [
                {"$addFields": {
                    "out_of_stock": {"$lt": ["$stock", 1]}
                }},
                self.build_stock_sort_pipeline_stage(),
                {"$project": {
                    "out_of_stock": 0,
                }}
            ]
        else:
            sort_pipeline_stage = []

        return sort_pipeline_stage
