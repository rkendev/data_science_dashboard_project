from .query_base import QueryBase


class Employee(QueryBase):
    # Set the class attribute `name` to the string "employee"
    name = "employee"

    # Query 3: select full name & employee_id for all employees in the DB.
    def names(self):
        """
        Returns a list of tuples: (full_name, employee_id)
        for all employees.
        """
        query_str = """
            SELECT (first_name || ' ' || last_name) AS full_name,
                   employee_id
            FROM employee
            ORDER BY employee_id
        """
        return self.run_query(query_str)

    # Define a method called `username` that receives an `id` argument
    # Query 4: select the employee's full name where employee_id = {id}.
    def username(self, id):
        """
        Returns a list of tuples: (full_name,)
        for the employee with the matching ID.
        """
        query_str = f"""
            SELECT (first_name || ' ' || last_name) AS full_name
            FROM employee
            WHERE employee_id = {id}
        """
        return self.run_query(query_str)

    # The method for the machine learning model data.
    def model_data(self, id):
        # Keep the SQL as is:
        query_string = f"""
            SELECT SUM(positive_events) positive_events
                 , SUM(negative_events) negative_events
            FROM {self.name}
            JOIN employee_events
                USING({self.name}_id)
            WHERE {self.name}.{self.name}_id = {id}
        """
        # Return a pandas DataFrame instead of just the string
        return self.pandas_query(query_string)