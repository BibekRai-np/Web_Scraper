"""
Web Scraper GUI - Graphical Interface for Single Page and Batch Scraping
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from datetime import datetime
import time
import os
import json
from pathlib import Path

class WebScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraper Pro - GUI Edition")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.is_scraping = False
        self.stop_scraping = False
        self.output_folder = "scraped_pages"
        
        # Create output folder if it doesn't exist
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        
        # Setup GUI
        self.setup_gui()
        
    def setup_gui(self):
        """Setup all GUI elements"""
        
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="📚 Web Scraper Pro", 
                               font=('Arial', 24, 'bold'), 
                               bg='#2c3e50', fg='white')
        title_label.pack(pady=20)
        
        # Main Notebook (Tabs)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Single Page Scraper
        self.single_tab = ttk.Frame(notebook)
        notebook.add(self.single_tab, text="🔗 Single Page")
        self.setup_single_tab()
        
        # Tab 2: Batch Scraper
        self.batch_tab = ttk.Frame(notebook)
        notebook.add(self.batch_tab, text="📚 Batch Scraper")
        self.setup_batch_tab()
        
        # Tab 3: Settings
        self.settings_tab = ttk.Frame(notebook)
        notebook.add(self.settings_tab, text="⚙️ Settings")
        self.setup_settings_tab()
        
        # Tab 4: History
        self.history_tab = ttk.Frame(notebook)
        notebook.add(self.history_tab, text="📜 History")
        self.setup_history_tab()
        
        # Status Bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg='#ecf0f1')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_single_tab(self):
        """Setup Single Page Scraper Tab"""
        
        # URL Input
        url_frame = tk.LabelFrame(self.single_tab, text="URL Input", padx=10, pady=10)
        url_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(url_frame, text="Enter URL:").grid(row=0, column=0, sticky='w')
        self.url_entry = tk.Entry(url_frame, width=70, font=('Arial', 10))
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)
        self.url_entry.insert(0, "https://")
        
        # Format Selection
        format_frame = tk.LabelFrame(self.single_tab, text="Output Format", padx=10, pady=10)
        format_frame.pack(fill='x', padx=10, pady=10)
        
        self.format_var = tk.StringVar(value="md")
        tk.Radiobutton(format_frame, text="Markdown (.md) - Compact", 
                       variable=self.format_var, value="md").pack(anchor='w')
        tk.Radiobutton(format_frame, text="Text (.txt) - Simple", 
                       variable=self.format_var, value="txt").pack(anchor='w')
        tk.Radiobutton(format_frame, text="JSON (.json) - Machine Readable", 
                       variable=self.format_var, value="json").pack(anchor='w')
        
        # Scrape Button
        button_frame = tk.Frame(self.single_tab)
        button_frame.pack(pady=10)
        
        self.scrape_button = tk.Button(button_frame, text="🚀 Scrape Page", 
                                       command=self.scrape_single_page,
                                       bg='#3498db', fg='white', 
                                       font=('Arial', 12, 'bold'),
                                       padx=20, pady=10)
        self.scrape_button.pack(side='left', padx=5)
        
        # Clear Button
        clear_button = tk.Button(button_frame, text="🗑️ Clear", 
                                 command=self.clear_output,
                                 bg='#95a5a6', fg='white',
                                 padx=20, pady=10)
        clear_button.pack(side='left', padx=5)
        
        # Output Area
        output_frame = tk.LabelFrame(self.single_tab, text="Output & Preview", padx=10, pady=10)
        output_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, 
                                                      width=80, height=20,
                                                      font=('Courier', 10))
        self.output_text.pack(fill='both', expand=True)
        
    def setup_batch_tab(self):
        """Setup Batch Scraper Tab"""
        
        # URLs File Selection
        file_frame = tk.LabelFrame(self.batch_tab, text="URLs File", padx=10, pady=10)
        file_frame.pack(fill='x', padx=10, pady=10)
        
        self.file_path_var = tk.StringVar()
        tk.Entry(file_frame, textvariable=self.file_path_var, width=60).pack(side='left', padx=5)
        
        browse_button = tk.Button(file_frame, text="Browse", 
                                  command=self.browse_urls_file,
                                  bg='#3498db', fg='white')
        browse_button.pack(side='left', padx=5)
        
        sample_button = tk.Button(file_frame, text="Create Sample", 
                                  command=self.create_sample_urls,
                                  bg='#2ecc71', fg='white')
        sample_button.pack(side='left', padx=5)
        
        # Batch Settings
        settings_frame = tk.LabelFrame(self.batch_tab, text="Batch Settings", padx=10, pady=10)
        settings_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(settings_frame, text="Delay (seconds):").grid(row=0, column=0, sticky='w', padx=5)
        self.delay_var = tk.StringVar(value="20")
        delay_spinbox = tk.Spinbox(settings_frame, from_=1, to=60, 
                                   textvariable=self.delay_var, width=10)
        delay_spinbox.grid(row=0, column=1, padx=5)
        
        tk.Label(settings_frame, text="Output Folder:").grid(row=1, column=0, sticky='w', padx=5)
        self.batch_output_var = tk.StringVar(value="scraped_pages")
        tk.Entry(settings_frame, textvariable=self.batch_output_var, width=30).grid(row=1, column=1, padx=5)
        
        # Progress
        progress_frame = tk.LabelFrame(self.batch_tab, text="Progress", padx=10, pady=10)
        progress_frame.pack(fill='x', padx=10, pady=10)
        
        self.progress_var = tk.StringVar(value="Ready")
        tk.Label(progress_frame, textvariable=self.progress_var).pack(anchor='w')
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.pack(fill='x', pady=5)
        
        # Batch Controls
        batch_button_frame = tk.Frame(self.batch_tab)
        batch_button_frame.pack(pady=10)
        
        self.start_batch_button = tk.Button(batch_button_frame, text="▶️ Start Batch Scraping", 
                                            command=self.start_batch_scraping,
                                            bg='#27ae60', fg='white',
                                            font=('Arial', 12, 'bold'),
                                            padx=20, pady=10)
        self.start_batch_button.pack(side='left', padx=5)
        
        self.stop_batch_button = tk.Button(batch_button_frame, text="⏹️ Stop", 
                                           command=self.stop_batch_scraping,
                                           bg='#e74c3c', fg='white',
                                           padx=20, pady=10,
                                           state='disabled')
        self.stop_batch_button.pack(side='left', padx=5)
        
        # Batch Output Log
        log_frame = tk.LabelFrame(self.batch_tab, text="Scraping Log", padx=10, pady=10)
        log_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.batch_log = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, 
                                                    width=80, height=15,
                                                    font=('Courier', 9))
        self.batch_log.pack(fill='both', expand=True)
        
    def setup_settings_tab(self):
        """Setup Settings Tab"""
        
        # Output Settings
        output_frame = tk.LabelFrame(self.settings_tab, text="Output Settings", padx=10, pady=10)
        output_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(output_frame, text="Default Output Folder:").grid(row=0, column=0, sticky='w')
        self.default_output_var = tk.StringVar(value="scraped_pages")
        tk.Entry(output_frame, textvariable=self.default_output_var, width=30).grid(row=0, column=1, padx=5)
        
        # User Agent Settings
        ua_frame = tk.LabelFrame(self.settings_tab, text="User Agent", padx=10, pady=10)
        ua_frame.pack(fill='x', padx=10, pady=10)
        
        self.ua_var = tk.StringVar(value="random")
        tk.Radiobutton(ua_frame, text="Random (Recommended)", 
                       variable=self.ua_var, value="random").pack(anchor='w')
        tk.Radiobutton(ua_frame, text="Custom", 
                       variable=self.ua_var, value="custom").pack(anchor='w')
        
        self.custom_ua_entry = tk.Entry(ua_frame, width=80)
        self.custom_ua_entry.pack(pady=5)
        self.custom_ua_entry.insert(0, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        self.custom_ua_entry.config(state='disabled')
        
        # Bind radio button to enable/disable custom entry
        def toggle_ua(*args):
            if self.ua_var.get() == "custom":
                self.custom_ua_entry.config(state='normal')
            else:
                self.custom_ua_entry.config(state='disabled')
        
        self.ua_var.trace('w', toggle_ua)
        
        # Timeout Settings
        timeout_frame = tk.LabelFrame(self.settings_tab, text="Timeout Settings", padx=10, pady=10)
        timeout_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(timeout_frame, text="Request Timeout (seconds):").pack(anchor='w')
        self.timeout_var = tk.StringVar(value="30")
        tk.Spinbox(timeout_frame, from_=10, to=120, textvariable=self.timeout_var, width=10).pack(anchor='w')
        
        # Save Settings Button
        save_button = tk.Button(self.settings_tab, text="💾 Save Settings", 
                               command=self.save_settings,
                               bg='#3498db', fg='white',
                               padx=20, pady=10)
        save_button.pack(pady=20)
        
    def setup_history_tab(self):
        """Setup History Tab"""
        
        # History Listbox
        history_frame = tk.LabelFrame(self.history_tab, text="Scraping History", padx=10, pady=10)
        history_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.history_listbox = tk.Listbox(history_frame, height=15)
        self.history_listbox.pack(fill='both', expand=True)
        
        # Buttons
        button_frame = tk.Frame(self.history_tab)
        button_frame.pack(pady=10)
        
        refresh_button = tk.Button(button_frame, text="🔄 Refresh", 
                                   command=self.load_history,
                                   padx=10, pady=5)
        refresh_button.pack(side='left', padx=5)
        
        open_button = tk.Button(button_frame, text="📂 Open File", 
                                command=self.open_selected_file,
                                padx=10, pady=5)
        open_button.pack(side='left', padx=5)
        
        delete_button = tk.Button(button_frame, text="🗑️ Delete", 
                                  command=self.delete_selected_file,
                                  padx=10, pady=5,
                                  bg='#e74c3c', fg='white')
        delete_button.pack(side='left', padx=5)
        
        # Load history
        self.load_history()
        
    def make_unique_filename(self, title, url, output_folder, extension='md'):
        """Create a unique filename using title and URL suffix"""
        # Clean title
        safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
        safe_title = re.sub(r'\s+', '_', safe_title.strip())[:100]  # limit length
        
        # Extract last 4 alphanumeric characters from URL
        url_clean = re.sub(r'[^a-zA-Z0-9]', '', url)
        if len(url_clean) >= 4:
            suffix = url_clean[-4:]  # last 4 alnum
        else:
            # fallback: use last 4 chars of the whole URL (including non-alnum)
            suffix = re.sub(r'[^a-zA-Z0-9]', '_', url)[-4:]
        
        base_filename = f"{safe_title}_{suffix}"
        filename = f"{output_folder}/{base_filename}.{extension}"
        
        # If file already exists, add a counter
        counter = 1
        while os.path.exists(filename):
            filename = f"{output_folder}/{base_filename}_{counter}.{extension}"
            counter += 1
        
        return filename
        
    def scrape_single_page(self):
        """Scrape a single page in a separate thread"""
        
        url = self.url_entry.get().strip()
        if not url or url == "https://":
            messagebox.showerror("Error", "Please enter a valid URL")
            return
        
        # Disable button during scraping
        self.scrape_button.config(state='disabled')
        self.status_bar.config(text="Scraping...")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "⏳ Scraping in progress...\n")
        
        # Run in thread
        thread = threading.Thread(target=self._scrape_single_page_thread, args=(url,))
        thread.daemon = True
        thread.start()
        
    def _scrape_single_page_thread(self, url):
        """Thread function for single page scraping"""
        
        try:
            # Add https:// if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Get user agent
            user_agent = self.get_user_agent()
            
            headers = {'User-Agent': user_agent}
            timeout = int(self.timeout_var.get())
            
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove clutter
            for element in soup(["script", "style", "nav", "header", "footer"]):
                element.decompose()
            
            # Get title
            title_tag = soup.find('title')
            title_text = title_tag.get_text().strip() if title_tag else "Untitled"
            
            # Get text
            text_content = []
            for p in soup.find_all('p'):
                text = p.get_text().strip()
                if text and len(text) > 20:
                    text_content.append(text)
            
            if not text_content:
                text_content = [line.strip() for line in soup.get_text().split('\n') if line.strip()]
            
            # Format based on selection
            format_type = self.format_var.get()
            
            if format_type == 'md':
                output = f"# {title_text}\n\n"
                output += f"**Source:** {url}\n"
                output += f"**Extracted:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                output += "---\n\n"
                output += '\n\n'.join(text_content)
                extension = 'md'
            elif format_type == 'json':
                output = json.dumps({
                    'title': title_text,
                    'url': url,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'content': '\n\n'.join(text_content),
                    'paragraphs': len(text_content)
                }, indent=2)
                extension = 'json'
            else:
                output = f"Title: {title_text}\n"
                output += f"Source: {url}\n"
                output += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                output += "=" * 50 + "\n\n"
                output += '\n\n'.join(text_content)
                extension = 'txt'
            
            # Save file with unique name
            filename = self.make_unique_filename(title_text, url, self.default_output_var.get(), extension)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(output)
            
            # Update UI
            self.root.after(0, self._update_single_page_result, 
                           True, title_text, filename, output[:1000])
            
        except Exception as e:
            self.root.after(0, self._update_single_page_result, 
                           False, str(e), "", "")
    
    def _update_single_page_result(self, success, message, filename, preview):
        """Update UI after single page scraping"""
        
        self.scrape_button.config(state='normal')
        
        if success:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"✅ SUCCESS!\n\n")
            self.output_text.insert(tk.END, f"📄 Title: {message}\n")
            self.output_text.insert(tk.END, f"💾 Saved to: {filename}\n\n")
            self.output_text.insert(tk.END, "📋 PREVIEW:\n")
            self.output_text.insert(tk.END, "-" * 50 + "\n")
            self.output_text.insert(tk.END, preview)
            if len(preview) >= 1000:
                self.output_text.insert(tk.END, "\n\n... (truncated)")
            
            self.status_bar.config(text=f"Success: Saved to {filename}")
            messagebox.showinfo("Success", f"Page scraped successfully!\nSaved to: {filename}")
            
            # Add to history
            self.load_history()
        else:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"❌ ERROR\n\n{message}")
            self.status_bar.config(text="Error occurred")
            messagebox.showerror("Error", f"Failed to scrape page:\n{message}")
    
    def browse_urls_file(self):
        """Browse for URLs file"""
        filename = filedialog.askopenfilename(
            title="Select URLs File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
            
            # Count URLs
            try:
                with open(filename, 'r') as f:
                    urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                self.progress_var.set(f"Found {len(urls)} URLs in file")
            except:
                pass
    
    def create_sample_urls(self):
        """Create sample URLs file"""
        filename = filedialog.asksaveasfilename(
            title="Create Sample URLs File",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        
        if filename:
            with open(filename, 'w') as f:
                f.write("# Sample URLs File\n")
                f.write("# Add your URLs below (one per line)\n")
                f.write("# Lines starting with # are ignored\n\n")
                f.write("https://example.com/article1\n")
                f.write("https://example.com/article2\n")
                f.write("https://example.com/article3\n")
            
            self.file_path_var.set(filename)
            messagebox.showinfo("Success", f"Sample file created:\n{filename}")
    
    def start_batch_scraping(self):
        """Start batch scraping in separate thread"""
        
        if not self.file_path_var.get():
            messagebox.showerror("Error", "Please select a URLs file first")
            return
        
        if self.is_scraping:
            messagebox.showwarning("Warning", "Scraping already in progress")
            return
        
        self.is_scraping = True
        self.stop_scraping = False
        self.start_batch_button.config(state='disabled')
        self.stop_batch_button.config(state='normal')
        self.batch_log.delete(1.0, tk.END)
        
        thread = threading.Thread(target=self._batch_scraping_thread)
        thread.daemon = True
        thread.start()
    
    def stop_batch_scraping(self):
        """Stop batch scraping"""
        self.stop_scraping = True
        self.log_message("⏹️ Stopping scraping... Please wait")
    
    def _batch_scraping_thread(self):
        """Thread function for batch scraping"""
        
        # Read URLs
        try:
            with open(self.file_path_var.get(), 'r') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except Exception as e:
            self.log_message(f"❌ Error reading file: {e}")
            self._batch_scraping_complete()
            return
        
        total_urls = len(urls)
        self.log_message(f"📊 Found {total_urls} URLs to scrape")
        
        # Create output folder
        output_folder = self.batch_output_var.get()
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        delay = int(self.delay_var.get())
        successful = 0
        failed = 0
        
        # Update progress bar
        self.root.after(0, lambda: self.progress_bar.config(maximum=total_urls))
        
        for i, url in enumerate(urls, 1):
            if self.stop_scraping:
                self.log_message("⚠️ Scraping stopped by user")
                break
            
            self.log_message(f"\n📌 [{i}/{total_urls}] Scraping: {url[:80]}...")
            
            try:
                # Scrape page
                user_agent = self.get_user_agent()
                headers = {'User-Agent': user_agent}
                timeout = int(self.timeout_var.get())
                
                response = requests.get(url, headers=headers, timeout=timeout)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove clutter
                for element in soup(["script", "style", "nav", "header", "footer"]):
                    element.decompose()
                
                # Get title
                title_tag = soup.find('title')
                title_text = title_tag.get_text().strip() if title_tag else "Untitled"
                
                # Get text
                text_content = []
                for p in soup.find_all('p'):
                    text = p.get_text().strip()
                    if text and len(text) > 20:
                        text_content.append(text)
                
                if not text_content:
                    text_content = [line.strip() for line in soup.get_text().split('\n') if line.strip()]
                
                # Create filename with uniqueness
                filename = self.make_unique_filename(title_text, url, output_folder, 'md')
                
                # Save file
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"# {title_text}\n\n")
                    f.write(f"**Source:** {url}\n")
                    f.write(f"**Extracted:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write("---\n\n")
                    f.write('\n\n'.join(text_content))
                
                successful += 1
                self.log_message(f"   ✅ Success - {len(text_content)} paragraphs")
                
            except Exception as e:
                failed += 1
                self.log_message(f"   ❌ Failed: {str(e)[:100]}")
            
            # Update progress
            self.root.after(0, lambda: self.progress_bar.config(value=i))
            self.root.after(0, lambda: self.progress_var.set(f"Progress: {i}/{total_urls}"))
            
            # Delay (except last)
            if i < total_urls and not self.stop_scraping:
                self.log_message(f"   ⏱️  Waiting {delay} seconds...")
                for remaining in range(delay, 0, -1):
                    if self.stop_scraping:
                        break
                    self.root.after(0, lambda r=remaining: self.progress_var.set(f"Waiting {r}s..."))
                    time.sleep(1)
        
        # Summary
        self.log_message("\n" + "=" * 50)
        self.log_message(f"📊 SCRAPING COMPLETE")
        self.log_message(f"✅ Successful: {successful}")
        self.log_message(f"❌ Failed: {failed}")
        self.log_message(f"📁 Files saved in: {output_folder}/")
        
        self._batch_scraping_complete()
    
    def _batch_scraping_complete(self):
        """Clean up after batch scraping"""
        self.is_scraping = False
        self.stop_scraping = False
        self.start_batch_button.config(state='normal')
        self.stop_batch_button.config(state='disabled')
        self.progress_var.set("Ready")
        messagebox.showinfo("Complete", "Batch scraping completed!")
    
    def log_message(self, message):
        """Add message to batch log"""
        self.root.after(0, lambda: self.batch_log.insert(tk.END, message + "\n"))
        self.root.after(0, lambda: self.batch_log.see(tk.END))
        self.root.after(0, lambda: self.status_bar.config(text=message[:100]))
    
    def get_user_agent(self):
        """Get user agent based on settings"""
        if self.ua_var.get() == "random":
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
            ]
            import random
            return random.choice(user_agents)
        else:
            return self.custom_ua_entry.get()
    
    def save_settings(self):
        """Save settings to file"""
        settings = {
            'output_folder': self.default_output_var.get(),
            'user_agent_mode': self.ua_var.get(),
            'custom_user_agent': self.custom_ua_entry.get(),
            'timeout': self.timeout_var.get()
        }
        
        with open('scraper_settings.json', 'w') as f:
            json.dump(settings, f, indent=2)
        
        messagebox.showinfo("Success", "Settings saved!")
    
    def load_history(self):
        """Load scraping history"""
        self.history_listbox.delete(0, tk.END)
        
        output_folder = self.default_output_var.get()
        if os.path.exists(output_folder):
            files = os.listdir(output_folder)
            for file in sorted(files, reverse=True)[:100]:  # Show last 100
                file_path = os.path.join(output_folder, file)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path)
                    modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                    self.history_listbox.insert(tk.END, f"{file} ({size:,} bytes, {modified.strftime('%Y-%m-%d')})")
    
    def open_selected_file(self):
        """Open selected file from history"""
        selection = self.history_listbox.curselection()
        if selection:
            filename = self.history_listbox.get(selection[0]).split(' ')[0]
            filepath = os.path.join(self.default_output_var.get(), filename)
            
            if os.path.exists(filepath):
                os.startfile(filepath)  # Windows
                # For Mac: os.system(f'open "{filepath}"')
                # For Linux: os.system(f'xdg-open "{filepath}"')
    
    def delete_selected_file(self):
        """Delete selected file from history"""
        selection = self.history_listbox.curselection()
        if selection:
            filename = self.history_listbox.get(selection[0]).split(' ')[0]
            filepath = os.path.join(self.default_output_var.get(), filename)
            
            if messagebox.askyesno("Confirm Delete", f"Delete {filename}?"):
                try:
                    os.remove(filepath)
                    self.load_history()
                    messagebox.showinfo("Success", "File deleted!")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not delete: {e}")
    
    def clear_output(self):
        """Clear output text area"""
        self.output_text.delete(1.0, tk.END)

def main():
    root = tk.Tk()
    app = WebScraperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()