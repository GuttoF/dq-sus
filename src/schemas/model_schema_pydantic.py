from griffe import check
import pandera as pa
from pandera.typing import Series

class NotificationsSchema(pa.DataFrameModel):
    TP_NOT: Series[int] = pa.Field(nullable=True)
    ID


    class Config:
        coerce = True
        nullable = False
        strict = True
        regex = False
        unique = False
        required = True