# fonts.py

def get_multiple_fonts_css():
    """
    Trả về CSS tùy chỉnh cho nhiều font từ Google Fonts với kích thước chữ.
    """
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');  /* Handwriting font */
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');  /* Display font */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap'); /* Serif font */
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

    .montserrat { 
        font-family: 'Montserrat', sans-serif; 
        font-size: 24px;
    }

    .monospace { 
        font-family: 'Roboto Mono', monospace; 
        font-size: 20px;
    }

    .handwriting { 
        font-family: 'Pacifico', cursive; 
        font-size: 60px;
    }

    .display { 
        font-family: 'Bebas Neue', sans-serif; 
        font-size: 36px;
    }

    .serif { 
        font-family: 'Playfair Display', serif; 
        font-size: 22px;
    }
     .bebas {
        font-family: 'Bebas Neue', sans-serif; font-size: 36px; 
    }
    </style>
    """
    return css