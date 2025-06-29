from flask import Flask, render_template, request, redirect, url_for, jsonify
import os

# Create Flask app with static folder configuration
app = Flask(__name__, 
           static_folder='static', 
           static_url_path='/static')

# Expanded recipe database with instructions
RECIPES = [
    {
        'id': 1,
        'name': 'Mediterranean Quinoa Salad',
        'image': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400',
        'cook_time': 20,
        'difficulty': 'Easy',
        'rating': 4.5,
        'meal_types': ['lunch', 'dinner'],
        'dietary': ['vegetarian', 'gluten_free'],
        'ingredients': ['quinoa', 'tomatoes', 'cucumber', 'feta_cheese', 'olive_oil', 'lemon', 'oregano', 'red_onion'],
        'description': 'Fresh and healthy Mediterranean salad perfect for any meal with vibrant flavors.',
        'instructions': [
            'Rinse quinoa under cold water and cook according to package directions',
            'Let quinoa cool completely in a large bowl',
            'Dice tomatoes, cucumber, and red onion into small pieces',
            'Crumble feta cheese into bite-sized pieces',
            'Whisk together olive oil, lemon juice, and oregano for dressing',
            'Combine all ingredients and toss with dressing',
            'Season with salt and pepper, chill for 30 minutes before serving'
        ]
    },
    {
        'id': 2,
        'name': 'Chocolate Chip Cookies',
        'image': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=400',
        'cook_time': 25,
        'difficulty': 'Easy',
        'rating': 4.8,
        'meal_types': ['dessert'],
        'dietary': ['vegetarian'],
        'ingredients': ['flour', 'butter', 'brown_sugar', 'eggs', 'chocolate_chips', 'vanilla_extract', 'baking_soda', 'salt'],
        'description': 'Classic homemade chocolate chip cookies that everyone loves - crispy edges, chewy centers.',
        'instructions': [
            'Preheat oven to 375°F (190°C)',
            'Cream together softened butter and brown sugar until fluffy',
            'Beat in eggs one at a time, then add vanilla extract',
            'In separate bowl, whisk together flour, baking soda, and salt',
            'Gradually mix dry ingredients into wet ingredients',
            'Fold in chocolate chips until evenly distributed',
            'Drop rounded tablespoons of dough onto ungreased baking sheets',
            'Bake for 9-11 minutes until golden brown around edges',
            'Cool on baking sheet for 5 minutes before transferring to wire rack'
        ]
    },
    {
        'id': 3,
        'name': 'Grilled Salmon with Herbs',
        'image': 'https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400',
        'cook_time': 15,
        'difficulty': 'Medium',
        'rating': 4.6,
        'meal_types': ['lunch', 'dinner'],
        'dietary': ['pescatarian', 'gluten_free'],
        'ingredients': ['salmon', 'dill', 'parsley', 'lemon', 'olive_oil', 'garlic', 'black_pepper', 'salt'],
        'description': 'Perfectly grilled salmon with fresh herbs and lemon - healthy and flavorful.',
        'instructions': [
            'Preheat grill to medium-high heat',
            'Pat salmon fillets dry and season with salt and pepper',
            'Mix minced garlic, chopped dill, parsley, and olive oil',
            'Brush herb mixture over salmon fillets',
            'Grill salmon skin-side down for 4-5 minutes',
            'Flip carefully and grill for another 3-4 minutes',
            'Check internal temperature reaches 145°F (63°C)',
            'Serve immediately with fresh lemon wedges'
        ]
    },
    {
        'id': 4,
        'name': 'Avocado Toast Supreme',
        'image': 'https://images.unsplash.com/photo-1541519869847-4dd70b24cf80?w=400',
        'cook_time': 5,
        'difficulty': 'Easy',
        'rating': 4.3,
        'meal_types': ['breakfast'],
        'dietary': ['vegetarian', 'vegan'],
        'ingredients': ['bread', 'avocado', 'lemon', 'olive_oil', 'tomatoes', 'black_pepper', 'sea_salt', 'red_pepper_flakes'],
        'description': 'Simple and nutritious avocado toast perfect for breakfast or light lunch.',
        'instructions': [
            'Toast bread slices until golden and crispy',
            'Cut avocado in half, remove pit, and scoop into bowl',
            'Mash avocado with fork, leaving some chunks for texture',
            'Add lemon juice, salt, and pepper to avocado',
            'Spread avocado mixture generously on toast',
            'Top with sliced tomatoes and drizzle with olive oil',
            'Sprinkle with red pepper flakes and enjoy immediately'
        ]
    },
    {
        'id': 5,
        'name': 'Chicken Stir Fry Delight',
        'image': 'https://images.unsplash.com/photo-1603360946369-dc9bb6258143?w=400',
        'cook_time': 18,
        'difficulty': 'Medium',
        'rating': 4.4,
        'meal_types': ['lunch', 'dinner'],
        'dietary': ['gluten_free'],
        'ingredients': ['chicken_breast', 'bell_peppers', 'broccoli', 'carrots', 'soy_sauce', 'ginger', 'garlic', 'sesame_oil', 'green_onions'],
        'description': 'Quick and healthy chicken stir fry with fresh vegetables and savory sauce.',
        'instructions': [
            'Cut chicken breast into bite-sized pieces',
            'Slice bell peppers, cut broccoli into florets, slice carrots',
            'Heat sesame oil in large wok or skillet over high heat',
            'Cook chicken pieces until golden and cooked through, remove',
            'Stir-fry vegetables starting with carrots, then broccoli, then peppers',
            'Add minced garlic and ginger, cook for 30 seconds',
            'Return chicken to pan, add soy sauce and toss everything',
            'Garnish with sliced green onions and serve over rice'
        ]
    },
    {
        'id': 6,
        'name': 'Vegan Pasta Primavera',
        'image': 'https://images.unsplash.com/photo-1621996346565-e3dbc353d2e5?w=400',
        'cook_time': 22,
        'difficulty': 'Easy',
        'rating': 4.2,
        'meal_types': ['lunch', 'dinner'],
        'dietary': ['vegan', 'dairy_free'],
        'ingredients': ['pasta', 'tomatoes', 'basil', 'garlic', 'olive_oil', 'nutritional_yeast', 'spinach', 'bell_peppers', 'zucchini'],
        'description': 'Delicious vegan pasta with fresh vegetables and herbs in a light, flavorful sauce.',
        'instructions': [
            'Cook pasta according to package directions until al dente',
            'Heat olive oil in large pan over medium heat',
            'Sauté diced bell peppers and zucchini until tender',
            'Add minced garlic and cook for 1 minute',
            'Add diced tomatoes and cook until softened',
            'Stir in fresh spinach until wilted',
            'Drain pasta and add to vegetable mixture',
            'Toss with fresh basil, nutritional yeast, salt and pepper',
            'Serve hot with extra nutritional yeast if desired'
        ]
    },
    {
        'id': 7,
        'name': 'Authentic Beef Tacos',
        'image': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400',
        'cook_time': 30,
        'difficulty': 'Medium',
        'rating': 4.7,
        'meal_types': ['lunch', 'dinner'],
        'dietary': [],
        'ingredients': ['ground_beef', 'tortillas', 'onions', 'cheddar', 'lettuce', 'tomatoes', 'cumin', 'paprika', 'chili_powder', 'lime'],
        'description': 'Flavorful beef tacos with fresh toppings and authentic Mexican spices.',
        'instructions': [
            'Heat large skillet over medium-high heat',
            'Brown ground beef, breaking it up as it cooks',
            'Add diced onions and cook until translucent',
            'Season with cumin, paprika, chili powder, salt and pepper',
            'Simmer for 10 minutes until flavors meld',
            'Warm tortillas in dry skillet or microwave',
            'Shred lettuce, dice tomatoes, and grate cheese',
            'Fill tortillas with beef mixture and desired toppings',
            'Serve with lime wedges and hot sauce'
        ]
    },
    {
        'id': 8,
        'name': 'Fluffy Pancakes',
        'image': 'https://images.unsplash.com/photo-1528207776546-365bb710ee93?w=400',
        'cook_time': 15,
        'difficulty': 'Easy',
        'rating': 4.5,
        'meal_types': ['breakfast'],
        'dietary': ['vegetarian'],
        'ingredients': ['flour', 'milk', 'eggs', 'sugar', 'baking_powder', 'butter', 'vanilla_extract', 'salt'],
        'description': 'Fluffy pancakes perfect for weekend breakfast with maple syrup.',
        'instructions': [
            'Whisk together flour, sugar, baking powder, and salt in large bowl',
            'In separate bowl, beat eggs and add milk, melted butter, and vanilla',
            'Pour wet ingredients into dry ingredients and stir until just combined',
            'Let batter rest for 5 minutes (some lumps are okay)',
            'Heat griddle or large skillet over medium heat',
            'Pour 1/4 cup batter for each pancake onto hot griddle',
            'Cook until bubbles form on surface, then flip',
            'Cook other side until golden brown',
            'Serve hot with butter and maple syrup'
        ]
    },
    {
        'id': 9,
        'name': 'Keto Cauliflower Rice',
        'image': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400',
        'cook_time': 12,
        'difficulty': 'Easy',
        'rating': 4.1,
        'meal_types': ['lunch', 'dinner'],
        'dietary': ['keto', 'vegetarian', 'gluten_free', 'low_carb'],
        'ingredients': ['cauliflower', 'butter', 'garlic', 'parsley', 'black_pepper', 'salt', 'onion_powder'],
        'description': 'Low-carb cauliflower rice that\'s perfect for keto diet and incredibly flavorful.',
        'instructions': [
            'Remove leaves and core from cauliflower head',
            'Cut into florets and pulse in food processor until rice-sized',
            'Heat butter in large skillet over medium heat',
            'Add minced garlic and cook for 30 seconds',
            'Add cauliflower rice and season with salt, pepper, onion powder',
            'Cook for 5-7 minutes, stirring frequently',
            'Remove from heat when tender but not mushy',
            'Stir in fresh chopped parsley before serving'
        ]
    },
    {
        'id': 10,
        'name': 'Tropical Fruit Smoothie',
        'image': 'https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=400',
        'cook_time': 3,
        'difficulty': 'Easy',
        'rating': 4.4,
        'meal_types': ['breakfast'],
        'dietary': ['vegetarian', 'vegan', 'gluten_free'],
        'ingredients': ['bananas', 'mango', 'pineapple', 'coconut_milk', 'honey', 'lime', 'ice'],
        'description': 'Refreshing tropical fruit smoothie packed with vitamins and natural sweetness.',
        'instructions': [
            'Peel and slice bananas, freeze for 30 minutes if desired',
            'Cut mango and pineapple into chunks',
            'Add all fruits to high-speed blender',
            'Pour in coconut milk and add honey to taste',
            'Squeeze fresh lime juice into blender',
            'Add handful of ice cubes for thickness',
            'Blend on high until smooth and creamy',
            'Taste and adjust sweetness as needed',
            'Serve immediately in chilled glasses'
        ]
    },
    {
        'id': 11,
        'name': 'Creamy Mushroom Risotto',
        'image': 'https://images.unsplash.com/photo-1476124369491-e7addf5db371?w=400',
        'cook_time': 35,
        'difficulty': 'Hard',
        'rating': 4.6,
        'meal_types': ['dinner'],
        'dietary': ['vegetarian'],
        'ingredients': ['arborio_rice', 'mushrooms', 'onions', 'garlic', 'white_wine', 'vegetable_broth', 'parmesan', 'butter', 'olive_oil'],
        'description': 'Rich and creamy mushroom risotto with authentic Italian flavors.',
        'instructions': [
            'Heat vegetable broth in saucepan and keep warm',
            'Slice mushrooms and sauté in olive oil until golden',
            'In separate pan, sauté diced onions until translucent',
            'Add minced garlic and arborio rice, stir for 2 minutes',
            'Pour in white wine and stir until absorbed',
            'Add warm broth one ladle at a time, stirring constantly',
            'Continue until rice is creamy and al dente (about 20 minutes)',
            'Stir in sautéed mushrooms, butter, and parmesan',
            'Season with salt and pepper, serve immediately'
        ]
    },
    {
        'id': 12,
        'name': 'Thai Green Curry',
        'image': 'https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?w=400',
        'cook_time': 25,
        'difficulty': 'Medium',
        'rating': 4.5,
        'meal_types': ['dinner'],
        'dietary': ['gluten_free'],
        'ingredients': ['chicken_thighs', 'coconut_milk', 'green_curry_paste', 'thai_basil', 'bell_peppers', 'bamboo_shoots', 'fish_sauce', 'lime'],
        'description': 'Authentic Thai green curry with tender chicken and vibrant vegetables.',
        'instructions': [
            'Cut chicken thighs into bite-sized pieces',
            'Heat 2 tbsp coconut milk in wok over medium heat',
            'Add green curry paste and fry until fragrant',
            'Add chicken pieces and cook until sealed',
            'Pour in remaining coconut milk and bring to simmer',
            'Add sliced bell peppers and bamboo shoots',
            'Season with fish sauce and simmer for 15 minutes',
            'Stir in Thai basil leaves and lime juice',
            'Serve hot over jasmine rice'
        ]
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Get form data
    search_term = request.form.get('search_term', '').lower()
    selected_ingredients = request.form.getlist('ingredients')
    meal_type = request.form.get('meal_type', '')
    dietary = request.form.get('dietary', '')
    cook_time = request.form.get('cook_time', '')
    
    # Filter recipes
    filtered_recipes = []
    
    for recipe in RECIPES:
        # Check if recipe matches search criteria
        matches = True
        
        # Text search in recipe name, description, and ingredients
        if search_term:
            search_fields = [
                recipe['name'].lower(),
                recipe['description'].lower()
            ] + [ingredient.lower() for ingredient in recipe['ingredients']]
            
            if not any(search_term in field for field in search_fields):
                matches = False
        
        # Filter by ingredients (recipe must contain at least one selected ingredient)
        if selected_ingredients and matches:
            if not any(ingredient in recipe['ingredients'] for ingredient in selected_ingredients):
                matches = False
        
        # Filter by meal type
        if meal_type and matches:
            if meal_type not in recipe['meal_types']:
                matches = False
        
        # Filter by dietary preferences
        if dietary and matches:
            if dietary not in recipe['dietary']:
                matches = False
        
        # Filter by cook time
        if cook_time and matches:
            if cook_time == 'quick' and recipe['cook_time'] > 15:
                matches = False
            elif cook_time == 'medium' and (recipe['cook_time'] < 15 or recipe['cook_time'] > 30):
                matches = False
            elif cook_time == 'long' and recipe['cook_time'] <= 30:
                matches = False
        
        if matches:
            filtered_recipes.append(recipe)
    
    # Sort results by rating (highest first)
    filtered_recipes.sort(key=lambda x: x['rating'], reverse=True)
    
    return render_template('result.html', 
                         recipes=filtered_recipes, 
                         search_term=search_term,
                         total_results=len(filtered_recipes))

@app.route('/style.css')
def serve_css():
    return app.send_static_file('style.css')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)