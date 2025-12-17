from flask import Flask, render_template_string

app = Flask(__name__)

# We store the HTML inside this Python string
HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gourmet Recipe Visualizer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
        body { background-color: #f9fafb; color: #1f2937; line-height: 1.6; }
        .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
        header { text-align: center; margin-bottom: 50px; }
        h1 { font-size: 2.5rem; color: #111; margin-bottom: 10px; }
        .subtitle { color: #6b7280; font-size: 1.1rem; }
        
        /* Filter Buttons */
        .filters { display: flex; justify-content: center; gap: 10px; margin-bottom: 40px; flex-wrap: wrap; }
        .filter-btn {
            background-color: #e5e7eb; color: #1f2937; border: none;
            padding: 12px 24px; border-radius: 50px; cursor: pointer;
            font-weight: 600; font-size: 0.95rem; transition: all 0.2s ease;
        }
        .filter-btn:hover { background-color: #d1d5db; transform: translateY(-2px); }
        .filter-btn.active { background-color: #e63946; color: white; box-shadow: 0 4px 10px rgba(230, 57, 70, 0.3); }

        /* Grid & Cards */
        .recipe-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 30px; }
        .recipe-card {
            background: white; border-radius: 16px; overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            display: flex; flex-direction: column;
        }
        .recipe-card:hover { transform: translateY(-5px); box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1); }
        .card-image { width: 100%; height: 220px; object-fit: cover; }
        .card-content { padding: 20px; flex-grow: 1; display: flex; flex-direction: column; }
        .recipe-title { font-size: 1.25rem; font-weight: 700; color: #111; margin-bottom: 10px; }
        .tags-container { display: flex; gap: 8px; margin-bottom: 15px; flex-wrap: wrap; }
        .tag {
            font-size: 0.75rem; padding: 4px 10px; border-radius: 12px;
            background-color: #f3f4f6; color: #4b5563; font-weight: 600; text-transform: uppercase;
        }
        .description { color: #4b5563; font-size: 0.95rem; margin-bottom: 20px; flex-grow: 1; }
        .time-tag { font-size: 0.85rem; color: #6b7280; }
        .view-btn {
            padding: 10px; background-color: white; border: 2px solid #e63946;
            color: #e63946; font-weight: bold; border-radius: 8px;
            cursor: pointer; transition: all 0.2s; width: 100%;
        }
        .view-btn:hover { background-color: #e63946; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Culinary Canvas</h1>
            <p class="subtitle">Visually stunning recipes for every palate</p>
        </header>
        <div class="filters">
            <button class="filter-btn active" data-filter="all">All Recipes</button>
            <button class="filter-btn" data-filter="Dinner">Dinner</button>
            <button class="filter-btn" data-filter="Breakfast">Breakfast</button>
            <button class="filter-btn" data-filter="Lunch">Lunch</button>
            <button class="filter-btn" data-filter="Dessert">Dessert</button>
            <button class="filter-btn" data-filter="Healthy">Healthy</button>
        </div>
        <div class="recipe-grid" id="recipeGrid"></div>
    </div>

    <script>
        const recipes = [
            { id: 1, title: "Creamy Tuscan Chicken", image: "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?auto=format&fit=crop&w=800&q=80", tags: ["Dinner", "Chicken", "Creamy"], time: "30 mins", description: "Golden chicken breasts in a rich garlic cream sauce with spinach and bursting cherry tomatoes." },
            { id: 2, title: "Rainbow Poke Bowl", image: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80", tags: ["Lunch", "Healthy", "Seafood"], time: "20 mins", description: "Fresh tuna, mango, avocado, and spicy mayo arranged in a stunning color wheel over sushi rice." },
            { id: 3, title: "Blood Orange Galette", image: "https://images.unsplash.com/photo-1614532661523-86a037b5f134?auto=format&fit=crop&w=800&q=80", tags: ["Dessert", "Fruit", "Baking"], time: "45 mins", description: "A rustic, sophisticated dessert featuring caramelized blood orange slices and fresh thyme." },
            { id: 4, title: "Golden Saffron Risotto", image: "https://images.unsplash.com/photo-1595908129746-25651b384433?auto=format&fit=crop&w=800&q=80", tags: ["Dinner", "Vegetarian", "Italian"], time: "40 mins", description: "A luxurious, vibrant yellow Italian classic featuring premium saffron threads and parmesan." },
            { id: 5, title: "Classic Smashburger", image: "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80", tags: ["Dinner", "Beef", "American"], time: "20 mins", description: "Crispy edges, juicy center, melted cheese, and toasted brioche buns. The ultimate comfort food." },
            { id: 6, title: "Avocado Toast & Egg", image: "https://images.unsplash.com/photo-1525351484164-8035a4206501?auto=format&fit=crop&w=800&q=80", tags: ["Breakfast", "Healthy", "Vegetarian"], time: "15 mins", description: "Creamy avocado on sourdough topped with a perfectly runny poached egg and chili flakes." }
        ];

        const grid = document.getElementById('recipeGrid');
        const filterBtns = document.querySelectorAll('.filter-btn');

        function displayRecipes(data) {
            grid.innerHTML = data.map(r => `
                <article class="recipe-card">
                    <img src="${r.image}" class="card-image">
                    <div class="card-content">
                        <h3 class="recipe-title">${r.title}</h3>
                        <div class="tags-container">${r.tags.map(t => `<span class="tag">${t}</span>`).join('')}</div>
                        <p class="description">${r.description}</p>
                        <div style="margin-top: auto; display: flex; justify-content: space-between; align-items: center;">
                            <span class="time-tag">⏱ ${r.time}</span>
                            <button class="view-btn">View Recipe</button>
                        </div>
                    </div>
                </article>
            `).join('');
        }

        displayRecipes(recipes);

        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const val = btn.getAttribute('data-filter');
                displayRecipes(val === 'all' ? recipes : recipes.filter(r => r.tags.includes(val)));
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
