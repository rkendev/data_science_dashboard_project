from .sql_execution import QueryMixin


# Define a class called QueryBase
class QueryBase(QueryMixin):
    # Create a class attribute called `name`
    # set the attribute to an empty string
    name = ""

    def names(self):
        """
        Returns an empty list.
        In child classes (Employee/Team),
        you might override or expand this logic.
        """
        return []

    def event_counts(self, id):
        """
        Returns a pandas DataFrame with the sum of positive and negative
        events grouped by event_date for the current entity (employee/team).
        Uses f-string formatting to reference {self.name}_id in the WHERE
        clause, and orders by event_date.
        """
        # QUERY 1
        # Summation of positive/negative events from 'employee_events'
        # grouped by event_date, filtering by the ID column
        query_string = f"""
        SELECT 
            event_date,
            SUM(positive_events) AS positive_events,
            SUM(negative_events) AS negative_events
        FROM employee_events
        WHERE {self.name}_id = {id}
        GROUP BY event_date
        ORDER BY event_date
        """
        return self.pandas_query(query_string)

    def notes(self, id):
        """
        Returns a pandas DataFrame of notes for the current entity
        (employee/team). Uses f-string formatting so the WHERE
        clause references {self.name}_id.
        """
        # QUERY 2
        # Retrieves note_date and note from the `notes` table,
        # filtering by the matching ID column.
        query_string = f"""
        SELECT 
            note_date, 
            note
        FROM notes
        WHERE notes.{self.name}_id = {id}
        ORDER BY note_date
        """
        return self.pandas_query(query_string)
