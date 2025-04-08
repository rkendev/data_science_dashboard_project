from .query_base import QueryBase


class Team(QueryBase):
    # Set the class attribute `name` to the string "team"
    name = "team"

    # Define a `names` method (Query 5)
    # that returns a list of tuples for all teams in the DB:
    # (team_name, team_id)
    def names(self):
        """
        Returns a list of tuples: (team_name, team_id)
        for all teams in the database.
        """
        query_str = """
            SELECT team_name, team_id
            FROM team
            ORDER BY team_id
        """
        return self.run_query(query_str)

    # Define a `username` method (Query 6)
    # that receives an ID argument, returning the team_name
    # for the corresponding team_id.
    def username(self, id):
        """
        Returns a list of tuples: (team_name,)
        for the team whose team_id matches the given ID.
        """
        query_str = f"""
            SELECT team_name
            FROM team
            WHERE team_id = {id}
        """
        return self.run_query(query_str)

    # Provide a DataFrame for the machine learning model data.
    # Keep the existing query, but call self.pandas_query(query_string).
    def model_data(self, id):
        query_string = f"""
            SELECT positive_events, negative_events FROM (
                SELECT employee_id
                     , SUM(positive_events) positive_events
                     , SUM(negative_events) negative_events
                FROM {self.name}
                JOIN employee_events
                    USING({self.name}_id)
                WHERE {self.name}.{self.name}_id = {id}
                GROUP BY employee_id
            )
        """
        return self.pandas_query(query_string)
