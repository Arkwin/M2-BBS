# Bulletin Board Database Functions

def store_bulletin_board(name, description=""):
    """Store a new bulletin board in the database."""
    try:
        bulletin_table_name = sanitize_string(mqtt_broker) + "_" + sanitize_string(root_topic) + sanitize_string(channel) + "_bulletin_boards"
        
        with sqlite3.connect(db_file_path) as db_connection:
            db_cursor = db_connection.cursor()
            
            timestamp = current_time()
            db_cursor.execute(f'''INSERT INTO {bulletin_table_name} 
                                (name, description, created_at, is_active)
                                VALUES (?, ?, ?, 1)''',
                            (name, description, timestamp))
            
            db_connection.commit()
            if debug:
                print(f"Bulletin board stored: {name}")
                
    except sqlite3.Error as e:
        print(f"SQLite error in store_bulletin_board: {e}")
    finally:
        db_connection.close()


def get_bulletin_boards():
    """Get all active bulletin boards."""
    try:
        bulletin_table_name = sanitize_string(mqtt_broker) + "_" + sanitize_string(root_topic) + sanitize_string(channel) + "_bulletin_boards"
        
        with sqlite3.connect(db_file_path) as db_connection:
            db_cursor = db_connection.cursor()
            
            db_cursor.execute(f'''SELECT id, name, description 
                                FROM {bulletin_table_name} 
                                WHERE is_active = 1 
                                ORDER BY name''')
            
            boards = db_cursor.fetchall()
            if debug:
                print(f"Retrieved {len(boards)} bulletin boards")
            
            return boards
                
    except sqlite3.Error as e:
        print(f"SQLite error in get_bulletin_boards: {e}")
        return []
    finally:
        db_connection.close()


def store_post(board_id, author_node_id, author_name, subject, content):
    """Store a new post in the database."""
    try:
        post_table_name = sanitize_string(mqtt_broker) + "_" + sanitize_string(root_topic) + sanitize_string(channel) + "_posts"
        
        with sqlite3.connect(db_file_path) as db_connection:
            db_cursor = db_connection.cursor()
            
            timestamp = current_time()
            db_cursor.execute(f'''INSERT INTO {post_table_name} 
                                (board_id, author_node_id, author_name, subject, content, timestamp, is_deleted)
                                VALUES (?, ?, ?, ?, ?, ?, 0)''',
                            (board_id, str(author_node_id), author_name, subject, content, timestamp))
            
            db_connection.commit()
            if debug:
                print(f"Post stored: {subject} by {author_name} in board {board_id}")
                
    except sqlite3.Error as e:
        print(f"SQLite error in store_post: {e}")
    finally:
        db_connection.close()


def get_posts_for_board(board_id):
    """Get all posts for a specific board."""
    try:
        post_table_name = sanitize_string(mqtt_broker) + "_" + sanitize_string(root_topic) + sanitize_string(channel) + "_posts"
        
        with sqlite3.connect(db_file_path) as db_connection:
            db_cursor = db_connection.cursor()
            
            db_cursor.execute(f'''SELECT id, author_name, subject, timestamp 
                                FROM {post_table_name} 
                                WHERE board_id = ? AND is_deleted = 0 
                                ORDER BY timestamp DESC''', (board_id,))
            
            posts = db_cursor.fetchall()
            if debug:
                print(f"Retrieved {len(posts)} posts for board {board_id}")
            
            return posts
                
    except sqlite3.Error as e:
        print(f"SQLite error in get_posts_for_board: {e}")
        return []
    finally:
        db_connection.close()


def get_post_content(post_id):
    """Get the full content of a specific post."""
    try:
        post_table_name = sanitize_string(mqtt_broker) + "_" + sanitize_string(root_topic) + sanitize_string(channel) + "_posts"
        
        with sqlite3.connect(db_file_path) as db_connection:
            db_cursor = db_connection.cursor()
            
            db_cursor.execute(f'''SELECT author_name, subject, content, timestamp 
                                FROM {post_table_name} 
                                WHERE id = ? AND is_deleted = 0''', (post_id,))
            
            post_data = db_cursor.fetchone()
            
            if post_data:
                if debug:
                    print(f"Retrieved post content for post ID {post_id}")
                
                return {
                    'author_name': post_data[0],
                    'subject': post_data[1],
                    'content': post_data[2],
                    'timestamp': post_data[3]
                }
            else:
                return None
                
    except sqlite3.Error as e:
        print(f"SQLite error in get_post_content: {e}")
        return None
    finally:
        db_connection.close()


def delete_post(post_id):
    """Mark a post as deleted."""
    try:
        post_table_name = sanitize_string(mqtt_broker) + "_" + sanitize_string(root_topic) + sanitize_string(channel) + "_posts"
        
        with sqlite3.connect(db_file_path) as db_connection:
            db_cursor = db_connection.cursor()
            
            db_cursor.execute(f'''UPDATE {post_table_name} 
                                SET is_deleted = 1 
                                WHERE id = ?''', (post_id,))
            
            db_connection.commit()
            if debug:
                print(f"Marked post ID {post_id} as deleted")
                
    except sqlite3.Error as e:
        print(f"SQLite error in delete_post: {e}")
    finally:
        db_connection.close()


def create_sample_bulletin_boards():
    """Create sample bulletin boards and posts for testing the system."""
    try:
        # Create sample boards
        sample_boards = [
            ("GENERAL", "General discussion and community topics"),
            ("ANNOUNCEMENTS", "Important announcements and system updates"),
            ("TECH", "Technical discussions and setup guides"),
            ("TEST", "Testing and development posts")
        ]
        
        # Store boards and get their IDs
        board_ids = {}
        for board_name, description in sample_boards:
            store_bulletin_board(board_name, description)
            # Get the board ID (we'll need to retrieve it)
            boards = get_bulletin_boards()
            for board in boards:
                if board[1] == board_name:  # board[1] is name
                    board_ids[board_name] = board[0]  # board[0] is id
                    break
        
        # Create sample posts
        sample_posts = {
            "GENERAL": [
                ("Welcome to DMV Mesh", "Welcome to DMV Mesh! Community-driven network serving the DMV area. Feel free to introduce yourself and explore the available features."),
                ("General Discussion", "General discussion thread for community topics, mesh networking, or casual conversation."),
                ("Community Guidelines", "Guidelines: Be respectful, avoid spam, follow local regulations, and help maintain a positive community.")
            ],
            "ANNOUNCEMENTS": [
                ("System Maintenance", "Maintenance: Sunday 2-4 AM. Some services may be temporarily unavailable. We apologize for any inconvenience."),
                ("New Features Available", "New features available: Improved routing and enhanced security. Check TECH board for details on setup and configuration."),
                ("Emergency Contact Info", "Emergency: Call 911. For mesh network issues, contact the admin team through the GENERAL board.")
            ],
            "TECH": [
                ("Meshtastic Setup Guide", "Setup: Install firmware, configure channels, set encryption keys, test connectivity. See detailed guide in TECH board."),
                ("Antenna Recommendations", "Antennas: 1/4 wave ground plane for base stations, flexible whip for mobile use. Height is more important than gain."),
                ("Battery Life Tips", "Battery tips: Use low power mode, disable GPS when not needed, use external power when stationary, and monitor battery levels.")
            ],
            "TEST": [
                ("Test Post 1", "This is test post 1 content for testing the bulletin board system."),
                ("Test Post 2", "This is test post 2 content for testing the bulletin board system."),
                ("Test Post 3", "This is test post 3 content for testing the bulletin board system.")
            ]
        }
        
        # Store posts
        for board_name, posts in sample_posts.items():
            if board_name in board_ids:
                board_id = board_ids[board_name]
                for subject, content in posts:
                    store_post(board_id, node_number, "System", subject, content)
        
        if debug:
            print(f"Created {len(sample_boards)} bulletin boards with sample posts")
            
    except Exception as e:
        if debug:
            print(f"Error creating sample bulletin boards: {str(e)}")


def get_board_by_name(board_name):
    """Get a bulletin board by name."""
    try:
        bulletin_table_name = sanitize_string(mqtt_broker) + "_" + sanitize_string(root_topic) + sanitize_string(channel) + "_bulletin_boards"
        
        with sqlite3.connect(db_file_path) as db_connection:
            db_cursor = db_connection.cursor()
            
            db_cursor.execute(f'''SELECT id, name, description 
                                FROM {bulletin_table_name} 
                                WHERE name = ? AND is_active = 1''', (board_name,))
            
            board = db_cursor.fetchone()
            return board
                
    except sqlite3.Error as e:
        print(f"SQLite error in get_board_by_name: {e}")
        return None
    finally:
        db_connection.close() 