import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime
from config import DB_CONFIG, TABLE_NAME

class DatabaseConnection:
    """Handle database connections and operations"""
    
    def __init__(self):
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    def get_all_records(self):
        """Fetch all records from the file table"""
        try:
            if not self.conn:
                self.connect()
            
            self.cursor.execute(f"SELECT * FROM {TABLE_NAME} ORDER BY id_file DESC;")
            records = self.cursor.fetchall()
            
            # Convert RealDictRow to regular dict for JSON serialization
            return [dict(record) for record in records]
        except Exception as e:
            print(f"Error fetching records: {e}")
            return []
    
    def insert_record(self, data):
        """Insert a new record into the database"""
        try:
            if not self.conn:
                self.connect()
            
            # Prepare the insertion
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            values = tuple(data.values())
            
            query = f"INSERT INTO {TABLE_NAME} ({columns}) VALUES ({placeholders}) RETURNING id_file;"
            
            self.cursor.execute(query, values)
            new_id = self.cursor.fetchone()['id_file']
            self.conn.commit()
            
            return True, new_id
        except Exception as e:
            self.conn.rollback()
            print(f"Error inserting record: {e}")
            return False, str(e)
    
    def update_record(self, record_id, data):
        """Update an existing record"""
        try:
            if not self.conn:
                self.connect()
            
            # Set update_date to current timestamp
            data['update_date'] = datetime.now()
            
            # Prepare the update query
            set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
            values = list(data.values())
            values.append(record_id)
            
            query = f"UPDATE {TABLE_NAME} SET {set_clause} WHERE id_file = %s;"
            
            self.cursor.execute(query, values)
            self.conn.commit()
            
            return True, "Record updated successfully"
        except Exception as e:
            self.conn.rollback()
            print(f"Error updating record: {e}")
            return False, str(e)
    
    def delete_record(self, record_id):
        """Delete a record"""
        try:
            if not self.conn:
                self.connect()
            
            query = f"DELETE FROM {TABLE_NAME} WHERE id_file = %s;"
            self.cursor.execute(query, (record_id,))
            self.conn.commit()
            
            return True, "Record deleted successfully"
        except Exception as e:
            self.conn.rollback()
            print(f"Error deleting record: {e}")
            return False, str(e)
    
    def get_record_by_id(self, record_id):
        """Fetch a specific record by ID"""
        try:
            if not self.conn:
                self.connect()
            
            self.cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id_file = %s;", (record_id,))
            record = self.cursor.fetchone()
            
            if record:
                return dict(record)
            return None
        except Exception as e:
            print(f"Error fetching record: {e}")
            return None


def get_db():
    """Factory function to get database connection"""
    return DatabaseConnection()
