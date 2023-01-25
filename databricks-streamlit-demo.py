class DataProvider:
  # above goes some low-level code
  def _get_data(self, query: str) -> pd.DataFrame:
      self.logger.debug(f"Running SQL query: {query}")
      start_time = dt.datetime.now()
      data = pd.read_sql(query, self.connection)
      end_time = dt.datetime.now()
      time_delta = end_time - start_time
      self.logger.debug(
          f"Query executed, returning the result. Total query time: {time_delta}"
      )
      return data
