import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime, timedelta
import random

class Node:
    """Node class for linked list implementation"""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """Linked List implementation for storing flashcards"""
    def __init__(self):
        self.head = None
        self.size = 0
    
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1
    
    def remove(self, card_id):
        if not self.head:
            return False
        
        if self.head.data['id'] == card_id:
            self.head = self.head.next
            self.size -= 1
            return True
        
        current = self.head
        while current.next:
            if current.next.data['id'] == card_id:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        return False
    
    def find(self, card_id):
        current = self.head
        while current:
            if current.data['id'] == card_id:
                return current.data
            current = current.next
        return None
    
    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def update(self, card_id, new_data):
        current = self.head
        while current:
            if current.data['id'] == card_id:
                current.data.update(new_data)
                return True
            current = current.next
        return False

class Stack:
    """Stack implementation for recently viewed cards"""
    def __init__(self, max_size=10):
        self.items = []
        self.max_size = max_size
    
    def push(self, item):
        if len(self.items) >= self.max_size:
            self.items.pop(0)  # Remove oldest item
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def get_all(self):
        return self.items.copy()

class Queue:
    """Queue implementation for study queue"""
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
    
    def peek(self):
        if not self.is_empty():
            return self.items[0]
        return None
    
    def get_all(self):
        return self.items.copy()

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Flashcard Study App")
        self.root.geometry("1000x700")
        self.root.configure(bg="#72148f")
        
        # Data structures
        self.flashcards = LinkedList()  # Main storage
        self.categories = {}  # Dictionary for categorization
        self.recent_cards = Stack(10)  # Recently viewed cards
        self.study_queue = Queue()  # Cards to study
        self.statistics = {
            'total_studied': 0,
            'correct_answers': 0,
            'wrong_answers': 0,
            'study_sessions': 0
        }
        
        # File for persistence
        self.data_file = "flashcards_data.json"
        
        # Load existing data
        self.load_data()
        
        # Create GUI
        self.create_widgets()
        
        # Populate study queue on startup
        self.populate_study_queue()
    
    def create_widgets(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_manage_tab()
        self.create_study_tab()
        self.create_statistics_tab()
        self.create_recent_tab()
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.update_status()
    
    def create_manage_tab(self):
        # Manage Cards Tab
        manage_frame = ttk.Frame(self.notebook)
        self.notebook.add(manage_frame, text="Manage Cards")
        
        # Left panel for CRUD operations
        left_panel = ttk.LabelFrame(manage_frame, text="Card Operations", padding=10)
        left_panel.pack(side='left', fill='y', padx=5, pady=5)
        
        # Create card section
        ttk.Label(left_panel, text="Front:", font=('Arial', 10, 'bold')).pack(anchor='w')
        self.front_entry = tk.Text(left_panel, height=3, width=30, wrap='word')
        self.front_entry.pack(pady=2)
        
        ttk.Label(left_panel, text="Back:", font=('Arial', 10, 'bold')).pack(anchor='w')
        self.back_entry = tk.Text(left_panel, height=3, width=30, wrap='word')
        self.back_entry.pack(pady=2)
        
        ttk.Label(left_panel, text="Category:", font=('Arial', 10, 'bold')).pack(anchor='w')
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(left_panel, textvariable=self.category_var, width=27)
        self.category_combo.pack(pady=2)
        self.update_category_combo()
        
        # CRUD Buttons
        button_frame = ttk.Frame(left_panel)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Create Card", command=self.create_card, 
                  style='Accent.TButton').pack(pady=2, fill='x')
        ttk.Button(button_frame, text="Update Card", command=self.update_card).pack(pady=2, fill='x')
        ttk.Button(button_frame, text="Delete Card", command=self.delete_card).pack(pady=2, fill='x')
        ttk.Button(button_frame, text="Clear Fields", command=self.clear_fields).pack(pady=2, fill='x')
        
        # Right panel for card list
        right_panel = ttk.LabelFrame(manage_frame, text="All Cards", padding=10)
        right_panel.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        # Search frame
        search_frame = ttk.Frame(right_panel)
        search_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").pack(side='left')
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_cards)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side='left', padx=5)
        
        ttk.Label(search_frame, text="Filter by Category:").pack(side='left', padx=(20, 5))
        self.filter_var = tk.StringVar()
        self.filter_var.trace('w', self.filter_cards)
        filter_combo = ttk.Combobox(search_frame, textvariable=self.filter_var, width=15)
        filter_combo.pack(side='left', padx=5)
        filter_combo['values'] = ['All'] + list(self.categories.keys())
        filter_combo.set('All')
        
        # Treeview for displaying cards
        columns = ('ID', 'Front', 'Back', 'Category', 'Difficulty', 'Last Studied')
        self.tree = ttk.Treeview(right_panel, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.tree.heading('ID', text='ID')
        self.tree.heading('Front', text='Front')
        self.tree.heading('Back', text='Back')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Difficulty', text='Difficulty')
        self.tree.heading('Last Studied', text='Last Studied')
        
        self.tree.column('ID', width=50)
        self.tree.column('Front', width=150)
        self.tree.column('Back', width=150)
        self.tree.column('Category', width=100)
        self.tree.column('Difficulty', width=80)
        self.tree.column('Last Studied', width=100)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(right_panel, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_card_select)
        
        self.refresh_card_list()
    
    def create_study_tab(self):
        # Study Tab
        study_frame = ttk.Frame(self.notebook)
        self.notebook.add(study_frame, text="Study Mode")
        
        # Study controls
        control_frame = ttk.LabelFrame(study_frame, text="Study Controls", padding=10)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(control_frame, text="Start Study Session", 
                  command=self.start_study_session, style='Accent.TButton').pack(side='left', padx=5)
        ttk.Button(control_frame, text="Next Card", command=self.next_card).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Previous Card", command=self.previous_card).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Shuffle Queue", command=self.shuffle_study_queue).pack(side='left', padx=5)
        
        # Study area
        self.study_area = ttk.LabelFrame(study_frame, text="Current Card", padding=20)
        self.study_area.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Card display
        self.card_front_label = tk.Label(self.study_area, text="Click 'Start Study Session' to begin", 
                                        font=('Arial', 16), wraplength=400, justify='center',
                                        bg='white', relief='raised', bd=2, height=8)
        self.card_front_label.pack(fill='both', expand=True, pady=10)
        
        # Study buttons
        study_button_frame = ttk.Frame(self.study_area)
        study_button_frame.pack(pady=10)
        
        ttk.Button(study_button_frame, text="Show Answer", 
                  command=self.show_answer).pack(side='left', padx=5)
        ttk.Button(study_button_frame, text="Mark as Easy", 
                  command=lambda: self.mark_difficulty('easy')).pack(side='left', padx=5)
        ttk.Button(study_button_frame, text="Mark as Hard", 
                  command=lambda: self.mark_difficulty('hard')).pack(side='left', padx=5)
        ttk.Button(study_button_frame, text="Mark as Wrong", 
                  command=lambda: self.mark_difficulty('wrong')).pack(side='left', padx=5)
        
        # Study queue info
        queue_frame = ttk.LabelFrame(study_frame, text="Study Queue", padding=10)
        queue_frame.pack(fill='x', padx=10, pady=5)
        
        self.queue_label = tk.Label(queue_frame, text="Queue: 0 cards")
        self.queue_label.pack()
        
        self.current_card = None
        self.showing_answer = False
    
    def create_statistics_tab(self):
        # Statistics Tab
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="Statistics")
        
        # Statistics display
        stats_display = ttk.LabelFrame(stats_frame, text="Study Statistics", padding=20)
        stats_display.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.stats_text = tk.Text(stats_display, height=20, width=60, font=('Courier', 11))
        self.stats_text.pack(fill='both', expand=True)
        
        # Refresh button
        ttk.Button(stats_display, text="Refresh Statistics", 
                  command=self.update_statistics_display).pack(pady=10)
        
        self.update_statistics_display()
    
    def create_recent_tab(self):
        # Recent Cards Tab
        recent_frame = ttk.Frame(self.notebook)
        self.notebook.add(recent_frame, text="Recent Cards")
        
        recent_display = ttk.LabelFrame(recent_frame, text="Recently Viewed Cards", padding=10)
        recent_display.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Recent cards listbox
        self.recent_listbox = tk.Listbox(recent_display, height=15, font=('Arial', 10))
        recent_scrollbar = ttk.Scrollbar(recent_display, orient='vertical', command=self.recent_listbox.yview)
        self.recent_listbox.configure(yscrollcommand=recent_scrollbar.set)
        
        self.recent_listbox.pack(side='left', fill='both', expand=True)
        recent_scrollbar.pack(side='right', fill='y')
        
        # Refresh button
        ttk.Button(recent_display, text="Refresh Recent Cards", 
                  command=self.update_recent_display).pack(pady=10)
        
        self.update_recent_display()
    
    def create_card(self):
        front = self.front_entry.get(1.0, tk.END).strip()
        back = self.back_entry.get(1.0, tk.END).strip()
        category = self.category_var.get().strip()
        
        if not front or not back:
            messagebox.showerror("Error", "Both front and back are required!")
            return
        
        if not category:
            category = "General"
        
        # Generate unique ID
        card_id = len(self.flashcards.to_list()) + 1
        
        card_data = {
            'id': card_id,
            'front': front,
            'back': back,
            'category': category,
            'difficulty': 'medium',
            'times_studied': 0,
            'correct_count': 0,
            'wrong_count': 0,
            'last_studied': None,
            'created_date': datetime.now().isoformat()
        }
        
        # Add to linked list
        self.flashcards.append(card_data)
        
        # Update categories dictionary
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(card_id)
        
        # Add to study queue
        self.study_queue.enqueue(card_data)
        
        self.clear_fields()
        self.refresh_card_list()
        self.update_category_combo()
        self.save_data()
        self.update_status()
        
        messagebox.showinfo("Success", "Card created successfully!")
    
    def update_card(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a card to update!")
            return
        
        item = self.tree.item(selection[0])
        card_id = int(item['values'][0])
        
        front = self.front_entry.get(1.0, tk.END).strip()
        back = self.back_entry.get(1.0, tk.END).strip()
        category = self.category_var.get().strip()
        
        if not front or not back:
            messagebox.showerror("Error", "Both front and back are required!")
            return
        
        if not category:
            category = "General"
        
        update_data = {
            'front': front,
            'back': back,
            'category': category
        }
        
        if self.flashcards.update(card_id, update_data):
            # Update categories
            self.rebuild_categories()
            self.refresh_card_list()
            self.update_category_combo()
            self.save_data()
            messagebox.showinfo("Success", "Card updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update card!")
    
    def delete_card(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a card to delete!")
            return
        
        item = self.tree.item(selection[0])
        card_id = int(item['values'][0])
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this card?"):
            if self.flashcards.remove(card_id):
                self.rebuild_categories()
                self.refresh_card_list()
                self.update_category_combo()
                self.save_data()
                self.clear_fields()
                messagebox.showinfo("Success", "Card deleted successfully!")
            else:
                messagebox.showerror("Error", "Failed to delete card!")
    
    def clear_fields(self):
        self.front_entry.delete(1.0, tk.END)
        self.back_entry.delete(1.0, tk.END)
        self.category_var.set("")
    
    def on_card_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            card_id = int(item['values'][0])
            card = self.flashcards.find(card_id)
            
            if card:
                self.front_entry.delete(1.0, tk.END)
                self.front_entry.insert(1.0, card['front'])
                self.back_entry.delete(1.0, tk.END)
                self.back_entry.insert(1.0, card['back'])
                self.category_var.set(card['category'])
    
    def refresh_card_list(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add all cards
        cards = self.flashcards.to_list()
        for card in cards:
            last_studied = card.get('last_studied', 'Never')
            if last_studied and last_studied != 'Never':
                try:
                    last_studied = datetime.fromisoformat(last_studied).strftime('%Y-%m-%d')
                except:
                    last_studied = 'Never'
            
            self.tree.insert('', 'end', values=(
                card['id'],
                card['front'][:30] + '...' if len(card['front']) > 30 else card['front'],
                card['back'][:30] + '...' if len(card['back']) > 30 else card['back'],
                card['category'],
                card['difficulty'],
                last_studied
            ))
    
    def filter_cards(self, *args):
        search_term = self.search_var.get().lower()
        category_filter = self.filter_var.get()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filter and add cards
        cards = self.flashcards.to_list()
        for card in cards:
            # Apply search filter
            if search_term and search_term not in card['front'].lower() and search_term not in card['back'].lower():
                continue
            
            # Apply category filter
            if category_filter != 'All' and card['category'] != category_filter:
                continue
            
            last_studied = card.get('last_studied', 'Never')
            if last_studied and last_studied != 'Never':
                try:
                    last_studied = datetime.fromisoformat(last_studied).strftime('%Y-%m-%d')
                except:
                    last_studied = 'Never'
            
            self.tree.insert('', 'end', values=(
                card['id'],
                card['front'][:30] + '...' if len(card['front']) > 30 else card['front'],
                card['back'][:30] + '...' if len(card['back']) > 30 else card['back'],
                card['category'],
                card['difficulty'],
                last_studied
            ))
    
    def update_category_combo(self):
        categories = list(self.categories.keys())
        self.category_combo['values'] = categories
        
        # Update filter combo too
        if hasattr(self, 'filter_var'):
            filter_combo = None
            for widget in self.root.winfo_children():
                if isinstance(widget, ttk.Notebook):
                    for tab in widget.tabs():
                        tab_widget = widget.nametowidget(tab)
                        for child in tab_widget.winfo_children():
                            if isinstance(child, ttk.LabelFrame) and "All Cards" in str(child):
                                for subchild in child.winfo_children():
                                    if isinstance(subchild, ttk.Frame):
                                        for combo in subchild.winfo_children():
                                            if isinstance(combo, ttk.Combobox) and len(combo['values']) > 0:
                                                combo['values'] = ['All'] + categories
                                                break
    
    def rebuild_categories(self):
        self.categories = {}
        cards = self.flashcards.to_list()
        for card in cards:
            category = card['category']
            if category not in self.categories:
                self.categories[category] = []
            self.categories[category].append(card['id'])
    
    def start_study_session(self):
        if self.study_queue.is_empty():
            self.populate_study_queue()
        
        if self.study_queue.is_empty():
            messagebox.showinfo("No Cards", "No cards available for study!")
            return
        
        self.statistics['study_sessions'] += 1
        self.next_card()
        self.update_status()
    
    def populate_study_queue(self):
        # Clear current queue
        self.study_queue = Queue()
        
        # Add all cards to study queue
        cards = self.flashcards.to_list()
        for card in cards:
            self.study_queue.enqueue(card)
        
        self.update_queue_display()
    
    def shuffle_study_queue(self):
        cards = self.study_queue.get_all()
        random.shuffle(cards)
        self.study_queue = Queue()
        for card in cards:
            self.study_queue.enqueue(card)
        self.update_queue_display()
        messagebox.showinfo("Shuffled", "Study queue has been shuffled!")
    
    def next_card(self):
        if self.study_queue.is_empty():
            messagebox.showinfo("Study Complete", "You've completed all cards in the study queue!")
            self.card_front_label.config(text="Study session complete!\nClick 'Start Study Session' to begin again.")
            return
        
        self.current_card = self.study_queue.dequeue()
        self.showing_answer = False
        
        # Add to recent cards stack
        self.recent_cards.push(self.current_card)
        
        # Display front of card
        self.card_front_label.config(
            text=f"Front:\n\n{self.current_card['front']}\n\nCategory: {self.current_card['category']}",
            bg='lightblue'
        )
        
        self.update_queue_display()
        self.update_recent_display()
    
    def previous_card(self):
        if self.recent_cards.is_empty():
            messagebox.showinfo("No Previous Card", "No previous cards available!")
            return
        
        # Get the last card from recent stack
        previous_card = self.recent_cards.pop()
        if previous_card:
            self.current_card = previous_card
            self.showing_answer = False
            self.card_front_label.config(
                text=f"Front:\n\n{self.current_card['front']}\n\nCategory: {self.current_card['category']}",
                bg='lightblue'
            )
            self.update_recent_display()
    
    def show_answer(self):
        if not self.current_card:
            messagebox.showwarning("No Card", "No card is currently being studied!")
            return
        
        if not self.showing_answer:
            self.card_front_label.config(
                text=f"Back:\n\n{self.current_card['back']}\n\nCategory: {self.current_card['category']}",
                bg='lightgreen'
            )
            self.showing_answer = True
        else:
            self.card_front_label.config(
                text=f"Front:\n\n{self.current_card['front']}\n\nCategory: {self.current_card['category']}",
                bg='lightblue'
            )
            self.showing_answer = False
    
    def mark_difficulty(self, difficulty):
        if not self.current_card:
            messagebox.showwarning("No Card", "No card is currently being studied!")
            return
        
        # Update card statistics
        card_id = self.current_card['id']
        update_data = {
            'difficulty': difficulty,
            'times_studied': self.current_card.get('times_studied', 0) + 1,
            'last_studied': datetime.now().isoformat()
        }
        
        if difficulty == 'wrong':
            update_data['wrong_count'] = self.current_card.get('wrong_count', 0) + 1
            self.statistics['wrong_answers'] += 1
        else:
            update_data['correct_count'] = self.current_card.get('correct_count', 0) + 1
            self.statistics['correct_answers'] += 1
        
        self.statistics['total_studied'] += 1
        
        # Update the card in linked list
        self.flashcards.update(card_id, update_data)
        
        # If marked as easy, don't add back to queue immediately
        if difficulty != 'easy':
            self.study_queue.enqueue(self.current_card)
        
        self.save_data()
        self.next_card()
        self.update_status()
    
    def update_queue_display(self):
        queue_size = self.study_queue.size()
        self.queue_label.config(text=f"Queue: {queue_size} cards")
    
    def update_recent_display(self):
        self.recent_listbox.delete(0, tk.END)
        recent_cards = self.recent_cards.get_all()
        for i, card in enumerate(reversed(recent_cards)):
            display_text = f"{i+1}. {card['front'][:40]}..." if len(card['front']) > 40 else f"{i+1}. {card['front']}"
            self.recent_listbox.insert(0, display_text)
    
    def update_statistics_display(self):
        self.stats_text.delete(1.0, tk.END)
        
        total_cards = len(self.flashcards.to_list())
        total_studied = self.statistics['total_studied']
        correct = self.statistics['correct_answers']
        wrong = self.statistics['wrong_answers']
        sessions = self.statistics['study_sessions']
        
        accuracy = (correct / total_studied * 100) if total_studied > 0 else 0
        
        stats_text = f"""
FLASHCARD STUDY STATISTICS
{'='*50}

Total Cards: {total_cards}
Study Sessions: {sessions}
Total Cards Studied: {total_studied}
Correct Answers: {correct}
Wrong Answers: {wrong}
Accuracy: {accuracy:.1f}%

CATEGORY BREAKDOWN:
{'-'*30}
"""
        
        for category, card_ids in self.categories.items():
            stats_text += f"{category}: {len(card_ids)} cards\n"
        
        stats_text += f"\nDIFFICULTY DISTRIBUTION:\n{'-'*30}\n"
        
        difficulty_count = {'easy': 0, 'medium': 0, 'hard': 0}
        cards = self.flashcards.to_list()
        for card in cards:
            difficulty = card.get('difficulty', 'medium')
            difficulty_count[difficulty] += 1
        
        for diff, count in difficulty_count.items():
            stats_text += f"{diff.capitalize()}: {count} cards\n"
        
        stats_text += f"\nRECENT ACTIVITY:\n{'-'*30}\n"
        recent_cards = self.recent_cards.get_all()
        if recent_cards:
            for i, card in enumerate(reversed(recent_cards[-5:])):  # Show last 5
                stats_text += f"{i+1}. {card['front'][:30]}...\n"
        else:
            stats_text += "No recent activity\n"
        
        self.stats_text.insert(1.0, stats_text)
    
    def update_status(self):
        total_cards = len(self.flashcards.to_list())
        queue_size = self.study_queue.size()
        recent_size = len(self.recent_cards.get_all())
        
        status = f"Cards: {total_cards} | Queue: {queue_size} | Recent: {recent_size} | Sessions: {self.statistics['study_sessions']}"
        self.status_bar.config(text=status)
    
    def save_data(self):
        data = {
            'flashcards': self.flashcards.to_list(),
            'categories': self.categories,
            'statistics': self.statistics
        }
        
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save data: {str(e)}")
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                
                # Load flashcards into linked list
                cards = data.get('flashcards', [])
                for card in cards:
                    self.flashcards.append(card)
                
                # Load categories
                self.categories = data.get('categories', {})
                
                # Load statistics
                self.statistics.update(data.get('statistics', {}))
                
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load data: {str(e)}")

def main():
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure custom styles
    style.configure('Accent.TButton', foreground='white', background='#007acc')
    style.map('Accent.TButton', background=[('active', '#005a9e')])
    
    app = FlashcardApp(root)
    
    # Handle window closing
    def on_closing():
        app.save_data()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()