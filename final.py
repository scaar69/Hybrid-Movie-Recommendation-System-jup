import tkinter as tk
from 'P:\PROJECTS\movie recommendation' import hybrid_recommendations

class MovieRecommendation(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('Tamil Movie Recommendation System')

        # Create the movie title label and input field
        self.title_label = tk.Label(self.master, text='Enter a Tamil movie title:')
        self.title_label.pack(side=tk.TOP, pady=10)
        self.title_input = tk.Entry(self.master)
        self.title_input.pack(side=tk.TOP)

        # Create the button to trigger the recommendation
        self.recommend_button = tk.Button(self.master, text='Get Recommendations', command=self.recommend)
        self.recommend_button.pack(side=tk.TOP, pady=10)

        # Create the label to display the recommended movies
        self.recommendation_label = tk.Label(self.master, text='')
        self.recommendation_label.pack(side=tk.TOP, pady=10)

    def recommend(self):
        # Get the movie title from the input field
        title = self.title_input.get()

        # Call the recommendation function from the recommendation program
        recommendations = hybrid_recommendations(title)

        # Display the recommended movies in the label
        text = 'Recommended Movies:\n\n'
        for movie in recommendations:
            text += f'{movie[0]} - {movie[1]}\n'
        self.recommendation_label.config(text=text)

if __name__ == '__main__':
    root = tk.Tk()
    app = MovieRecommendation(root)
    app.pack()
    root.mainloop()
