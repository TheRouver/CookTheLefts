// Toast Notification Function
function showToast(message, type = 'success') {
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.style.position = 'fixed';
        container.style.bottom = '1rem';
        container.style.right = '1rem';
        container.style.zIndex = '1050';
        document.body.appendChild(container);
        toastContainer = container;
    }

    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type}`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');

    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" 
                    data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    toastContainer.appendChild(toast);

    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: 3000
    });
    bsToast.show();

    toast.addEventListener('hidden.bs.toast', function () {
        toast.remove();
    });
}

// Form Validation Helper
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }

        field.addEventListener('input', function() {
            if (this.value.trim()) {
                this.classList.remove('is-invalid');
            }
        });
    });

    return isValid;
}

// Loading State Helper
function setLoadingState(button, isLoading) {
    if (isLoading) {
        button.disabled = true;
        const originalText = button.innerHTML;
        button.setAttribute('data-original-text', originalText);
        button.innerHTML = `
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Lädt...
        `;
    } else {
        button.disabled = false;
        const originalText = button.getAttribute('data-original-text');
        if (originalText) {
            button.innerHTML = originalText;
        }
    }
}

// Recipe Search Functionality
function initializeRecipeSearch() {
    const ingredientsInput = document.getElementById('ingredients-input');
    const addIngredientButton = document.getElementById('add-ingredient');
    const searchButton = document.getElementById('search-button');
    const ingredientsTags = document.getElementById('ingredients-tags');
    const searchResults = document.getElementById('search-results');
    const resultsContainer = document.getElementById('results-container');
    let ingredients = new Set();

    if (!ingredientsInput || !addIngredientButton || !searchButton || !ingredientsTags || !searchResults || !resultsContainer) {
        console.error('Required elements not found');
        return;
    }

    // Make ingredients available globally for the modal
    window.ingredients = ingredients;

    function addIngredient(ingredient) {
        ingredient = ingredient.trim().toLowerCase();
        if (!ingredient) {
            showToast('Please enter an ingredient', 'warning');
            return;
        }
        
        // Basic validation
        if (ingredient.length < 2) {
            showToast('Ingredient name is too short', 'warning');
            return;
        }
        
        if (ingredients.has(ingredient)) {
            showToast('This ingredient is already added', 'warning');
            return;
        }
        
        ingredients.add(ingredient);
        updateTags();
        ingredientsInput.value = '';
        ingredientsInput.focus();
    }

    function removeIngredient(ingredient) {
        ingredients.delete(ingredient);
        updateTags();
    }

    function updateTags() {
        ingredientsTags.innerHTML = Array.from(ingredients).map(ingredient => `
            <span class="badge bg-primary me-2 mb-2 p-2">
                ${ingredient}
                <button type="button" class="btn-close btn-close-white ms-2" 
                        aria-label="Remove" onclick="removeIngredient('${ingredient}')"></button>
            </span>
        `).join('');

        searchButton.disabled = ingredients.size === 0;
    }

    function renderRecipeCard(recipe, isApiRecipe = true) {
        const dietaryTags = [];
        if (recipe.vegetarian) dietaryTags.push('<span class="badge bg-success me-1">Vegetarian</span>');
        if (recipe.vegan) dietaryTags.push('<span class="badge bg-success me-1">Vegan</span>');
        if (recipe.gluten_free) dietaryTags.push('<span class="badge bg-info me-1">Gluten-Free</span>');
        if (recipe.dairy_free) dietaryTags.push('<span class="badge bg-info me-1">Dairy-Free</span>');

        return `
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    ${recipe.image_url || recipe.image_path 
                        ? `<img src="${isApiRecipe ? recipe.image_url : recipe.image_path}" 
                               class="card-img-top" alt="${recipe.title}" 
                               style="height: 200px; object-fit: cover;">`
                        : `<div class="default-recipe-image">
                               <i class="bi bi-camera"></i>
                           </div>`
                    }
                    <div class="card-body">
                        <h5 class="card-title">${recipe.title}</h5>
                        <div class="progress mb-2">
                            <div class="progress-bar" role="progressbar" 
                                 style="width: ${recipe.match_percentage}%">
                                ${Math.round(recipe.match_percentage)}% Match
                            </div>
                        </div>
                        ${isApiRecipe 
                            ? `<p class="card-text">
                                   <small class="text-muted">
                                       <i class="bi bi-globe"></i> ${recipe.area}<br>
                                       <i class="bi bi-tag"></i> ${recipe.category}<br>
                                       <i class="bi bi-clock"></i> ${recipe.ready_in_minutes} mins
                                       <i class="bi bi-people"></i> ${recipe.servings} servings
                                   </small>
                               </p>
                               <div class="dietary-tags mb-2">
                                   ${dietaryTags.join('')}
                               </div>`
                            : `<p class="card-text">
                                   <small class="text-muted">
                                       <i class="bi bi-person"></i> ${recipe.author}<br>
                                       <i class="bi bi-heart-fill text-danger"></i> ${recipe.likes_count} Likes
                                   </small>
                               </p>`
                        }
                        <div class="ingredients mt-2">
                            <small class="text-success">
                                <i class="bi bi-check-circle"></i> Matching ingredients:<br>
                                ${recipe.matching_ingredients && recipe.matching_ingredients.length > 0 
                                    ? recipe.matching_ingredients.join(', ') 
                                    : 'No matching ingredients'}
                            </small>
                        </div>
                        <div class="mt-2">
                            <small class="text-danger">
                                <i class="bi bi-x-circle"></i> Missing ingredients:<br>
                                ${isApiRecipe 
                                    ? recipe.missing_ingredients.join(', ')
                                    : recipe.missing_ingredients.join(', ')
                                }
                            </small>
                        </div>
                        <div class="mt-3">
                            ${isApiRecipe
                                ? `<button class="btn btn-outline-primary btn-sm view-recipe"
                                          data-recipe-id="${recipe.id}"
                                          data-recipe-source="api">
                                       View Recipe
                                   </button>
                                   ${recipe.youtube_url 
                                       ? `<a href="${recipe.youtube_url}" 
                                            target="_blank" 
                                            class="btn btn-outline-danger btn-sm">
                                            <i class="bi bi-youtube"></i> Video
                                          </a>` 
                                       : ''}`
                                : `<a href="/recipes/${recipe.id}" 
                                     class="btn btn-outline-primary btn-sm">
                                     View Recipe
                                  </a>`
                            }
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    function displayResults(data) {
        // Handle API errors
        if (data.error) {
            resultsContainer.innerHTML = `
                <div class="col-12 text-center">
                    <p class="text-danger">
                        <i class="bi bi-exclamation-triangle"></i> ${data.error}
                    </p>
                    <p class="text-muted">Please try again with different ingredients or contact support if the problem persists.</p>
                </div>
            `;
            searchResults.style.display = 'block';
            return;
        }

        // Handle no results
        if ((!data.api_results || data.api_results.length === 0) && 
            (!data.user_results || data.user_results.length === 0)) {
            resultsContainer.innerHTML = `
                <div class="col-12 text-center">
                    <p class="text-muted">
                        <i class="bi bi-info-circle"></i> No recipes found with these ingredients.
                    </p>
                    <p>Suggestions:</p>
                    <ul class="list-unstyled">
                        <li>Try using fewer ingredients</li>
                        <li>Check ingredient spelling</li>
                        <li>Use more common ingredients</li>
                    </ul>
                </div>
            `;
            searchResults.style.display = 'block';
            return;
        }

        let html = '';

        // Display API results first
        if (data.api_results && data.api_results.length > 0) {
            html += `
                <div class="col-12">
                    <h3 class="mb-4">API Recipes</h3>
                </div>
                ${data.api_results.map(recipe => renderRecipeCard(recipe, true)).join('')}
            `;
        }

        // Display user results
        if (data.user_results && data.user_results.length > 0) {
            html += `
                <div class="col-12">
                    <h3 class="mt-4 mb-4">Community Recipes</h3>
                </div>
                ${data.user_results.map(recipe => renderRecipeCard(recipe, false)).join('')}
            `;
        }

        resultsContainer.innerHTML = html;
        searchResults.style.display = 'block';
        searchResults.scrollIntoView({ behavior: 'smooth' });
    }

    // Handle form submission for adding ingredients
    const form = document.getElementById('ingredients-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const input = document.getElementById('ingredients-input');
            const value = input ? input.value : '';
            
            if (value && value.trim()) {
                addIngredient(value);
            }
        });
    }

    // Search button click handler
    searchButton.addEventListener('click', async function() {
        if (ingredients.size === 0) {
            showToast('Please add at least one ingredient', 'warning');
            return;
        }

        setLoadingState(searchButton, true);
        searchResults.style.display = 'none';
        
        try {
            const searchUrl = `/search?ingredients=${Array.from(ingredients).join(',')}`;
            console.log('Searching with URL:', searchUrl);
            
            const response = await fetch(searchUrl);
            console.log('Search response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`Search request failed with status ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Search results:', data);
            
            if (data.error) {
                console.error('Search error:', data.error);
                showToast(data.error, 'danger');
                searchResults.style.display = 'none';
            } else if (data.success) {
                console.log('Displaying results:', {
                    apiResults: data.api_results?.length || 0,
                    userResults: data.user_results?.length || 0
                });
                if (data.message) {
                    console.log('Search message:', data.message);
                }
                displayResults({
                    api_results: data.api_results || [],
                    user_results: data.user_results || []
                });
            } else {
                console.error('Unexpected response format:', data);
                showToast('An error occurred while searching recipes', 'danger');
                searchResults.style.display = 'none';
            }
        } catch (error) {
            console.error('Search error:', error);
            showToast('Failed to search recipes. Please try again.', 'danger');
            searchResults.style.display = 'none';
        } finally {
            setLoadingState(searchButton, false);
            searchButton.disabled = ingredients.size === 0;
        }
    });

    // Initialize search button state
    searchButton.disabled = true;

    // Make removeIngredient available globally
    window.removeIngredient = removeIngredient;

    // Add input validation
    ingredientsInput.addEventListener('input', function(e) {
        const value = e.target.value.trim();
        if (value.length > 0 && value.length < 2) {
            e.target.classList.add('is-invalid');
        } else {
            e.target.classList.remove('is-invalid');
        }
    });
}

// Wait for DOM to be fully loaded
window.addEventListener('load', function() {
    // Initialize recipe search
    initializeRecipeSearch();

    // Initialize Bootstrap Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Handle recipe modal display
    document.addEventListener('click', async function(e) {
        if (e.target.classList.contains('view-recipe') || 
            e.target.closest('.view-recipe')) {
            const button = e.target.classList.contains('view-recipe') 
                ? e.target 
                : e.target.closest('.view-recipe');
            const recipeId = button.dataset.recipeId;
            const source = button.dataset.recipeSource;
            
            try {
                const response = await fetch(`/recipes/${recipeId}?source=${source}`, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                if (!response.ok) {
                    throw new Error('Failed to fetch recipe');
                }
                
                const recipe = await response.json();
                const modal = document.getElementById('recipeModal');
                
                if (!modal) {
                    console.error('Recipe modal not found');
                    return;
                }

                const modalTitle = modal.querySelector('.modal-title');
                const modalBody = modal.querySelector('.modal-body');
                
                if (!modalTitle || !modalBody) {
                    console.error('Modal elements not found');
                    return;
                }

                modalTitle.textContent = recipe.title;
                
                // Get current ingredients if any
                const currentIngredients = Array.from(window.ingredients || []).map(ing => ing.toLowerCase());
                
                // Separate ingredients into available and missing
                const availableIngredients = [];
                const missingIngredients = [];
                
                recipe.ingredients.forEach(ing => {
                    const ingredient = ing.ingredient.toLowerCase();
                    if (currentIngredients.some(current => ingredient.includes(current))) {
                        availableIngredients.push(ing);
                    } else {
                        missingIngredients.push(ing);
                    }
                });

                // Add dietary tags
                const dietaryTags = [];
                if (recipe.vegetarian) dietaryTags.push('<span class="badge bg-success me-1">Vegetarian</span>');
                if (recipe.vegan) dietaryTags.push('<span class="badge bg-success me-1">Vegan</span>');
                if (recipe.gluten_free) dietaryTags.push('<span class="badge bg-info me-1">Gluten-Free</span>');
                if (recipe.dairy_free) dietaryTags.push('<span class="badge bg-info me-1">Dairy-Free</span>');
                
                modalBody.innerHTML = `
                    ${recipe.image_url 
                        ? `<img src="${recipe.image_url}" class="img-fluid mb-3" alt="${recipe.title}">`
                        : `<div class="default-recipe-image mb-3">
                               <i class="bi bi-camera"></i>
                           </div>`
                    }
                    
                    <div class="dietary-tags mb-3">
                        ${dietaryTags.join('')}
                    </div>

                    <div class="recipe-meta mb-3">
                        <span class="me-3"><i class="bi bi-clock"></i> ${recipe.ready_in_minutes} mins</span>
                        <span><i class="bi bi-people"></i> ${recipe.servings} servings</span>
                    </div>
                    
                    <div class="row mb-4">
                        <div class="col-md-6">
                            <h6 class="text-success"><i class="bi bi-check-circle"></i> Available Ingredients:</h6>
                            <ul class="text-success">
                                ${availableIngredients.map(ing => 
                                    `<li>${ing.measure} ${ing.ingredient}</li>`).join('')}
                            </ul>
                        </div>
                        <div class="col-md-6">
                            <h6 class="text-danger"><i class="bi bi-x-circle"></i> Missing Ingredients:</h6>
                            <ul class="text-danger">
                                ${missingIngredients.map(ing => 
                                    `<li>${ing.measure} ${ing.ingredient}</li>`).join('')}
                            </ul>
                        </div>
                    </div>

                    <h6>Instructions:</h6>
                    <ol class="instructions-list">
                        ${Array.isArray(recipe.instructions) 
                            ? recipe.instructions.map(step => `<li class="mb-2">${step}</li>`).join('')
                            : `<li>${recipe.instructions}</li>`}
                    </ol>
                    ${recipe.source ? `<p><small>Source: <a href="${recipe.source}" 
                                                           target="_blank">Original Recipe</a></small></p>` : ''}
                `;
                
                const bsModal = new bootstrap.Modal(modal);
                bsModal.show();
            } catch (error) {
                console.error('Error fetching recipe:', error);
                showToast('Failed to load recipe details', 'danger');
            }
        }
    });
});
