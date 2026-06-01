document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tab[data-tab]');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.getAttribute('data-tab');
            
            if (!targetTab) return;
            
            const targetElement = document.getElementById(targetTab);
            if (!targetElement) return;
            
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            tab.classList.add('active');
            targetElement.classList.add('active');
        });
    });
});
