import tkinter as tk
from tkinter import messagebox
from tkinter import font
from collections import Counter
import heapq

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCoding:
    def __init__(self):
        self.codes = {}
        self.reverse_mapping = {}

    def build_huffman_tree(self, text):
        frequency = Counter(text)
        priority_queue = [Node(char, freq) for char, freq in frequency.items()]
        heapq.heapify(priority_queue)

        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)
            merged = Node(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(priority_queue, merged)

        self.build_codes(priority_queue[0], "")

    def build_codes(self, root, current_code):
        if root is None:
            return
        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
        self.build_codes(root.left, current_code + "0")
        self.build_codes(root.right, current_code + "1")

    def encode(self, text):
        encoded_output = ""
        for char in text:
            encoded_output += self.codes[char]
        return encoded_output

    def decode(self, encoded_text):
        current_code = ""
        decoded_output = ""
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                decoded_output += self.reverse_mapping[current_code]
                current_code = ""
        return decoded_output

class HuffmanUI:
    def __init__(self, master):
        self.master = master
        self.huffman_coding = HuffmanCoding()
        self.setup_ui()

    def setup_ui(self):
        self.master.title("Huffman Coding")

        # Load and set background image
        self.bg_image = tk.PhotoImage(file="D:/MCA CU/DAA/bg.png")  # Ensure this path is correct
        self.bg_canvas = tk.Canvas(self.master, width=600, height=600)
        self.bg_canvas.pack(fill="both", expand=True)

        # Display the background image on the canvas
        self.bg_canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Create a frame to hold the widgets, layering it on top of the canvas
        self.frame = tk.Frame(self.master, bg="#ffffff", bd=5)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Define custom fonts
        label_font = font.Font(family="Helvetica", size=14, weight="bold")
        button_font = font.Font(family="Helvetica", size=12, weight="bold")
        result_font = font.Font(family="Courier", size=10)

        # Add widgets with custom fonts
        self.label = tk.Label(self.frame, text="Enter text:", bg="#ffffff", font=label_font)
        self.label.pack(pady=5)

        self.text_entry = tk.Text(self.frame, height=5, width=40, font=result_font)
        self.text_entry.pack(pady=5)

        self.encode_button = tk.Button(self.frame, text="Encode", command=self.encode_text, font=button_font, bg="#4CAF50", fg="white")
        self.encode_button.pack(pady=5)

        self.decode_button = tk.Button(self.frame, text="Decode", command=self.decode_text, font=button_font, bg="#2196F3", fg="white")
        self.decode_button.pack(pady=5)

        self.result_label = tk.Label(self.frame, text="Result:", bg="#ffffff", font=label_font)
        self.result_label.pack(pady=5)

        self.result_display = tk.Text(self.frame, height=10, width=50, font=result_font, bg="#f0f0f0")
        self.result_display.pack(pady=5)

    def encode_text(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Input Error", "Please enter some text to encode.")
            return

        # Build Huffman Tree and encode text
        self.huffman_coding.build_huffman_tree(text)
        encoded_text = self.huffman_coding.encode(text)

        # Calculate original and encoded sizes
        original_bits = len(text) * 8  # 8 bits per character in ASCII
        encoded_bits = len(encoded_text)  # 1 bit per character in encoded binary string

        # Calculate compression ratio
        compression_ratio = (1 - (encoded_bits / original_bits)) * 100

        # Display results
        self.result_display.delete("1.0", tk.END)
        self.result_display.insert(tk.END, f"Encoded: {encoded_text}\n")
        self.result_display.insert(tk.END, "Huffman Codes:\n" + str(self.huffman_coding.codes) + "\n\n")
        self.result_display.insert(tk.END, f"Original Size: {original_bits} bits\n")
        self.result_display.insert(tk.END, f"Encoded Size: {encoded_bits} bits\n")
        self.result_display.insert(tk.END, f"Compression Ratio: {compression_ratio:.2f}%\n")

    def decode_text(self):
        try:
            encoded_text = self.result_display.get("1.0", tk.END).strip().split("\n")[0].split(": ")[1]
            if not encoded_text:
                messagebox.showerror("Input Error", "No encoded text to decode.")
                return
            decoded_text = self.huffman_coding.decode(encoded_text)
            self.result_display.insert(tk.END, f"\nDecoded: {decoded_text}")
        except IndexError:
            messagebox.showerror("Decode Error", "Could not find encoded text for decoding.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanUI(root)
    root.geometry("600x600")  # Set window size for better display
    root.mainloop()
