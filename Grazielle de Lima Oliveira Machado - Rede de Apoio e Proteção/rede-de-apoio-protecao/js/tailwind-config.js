/* Configuração do Tailwind (cores e fontes da identidade visual) */
if (window.tailwind) tailwind.config = {
  theme: { extend: {
    colors: {
      bgMain:'#F2F2F2', cardBg:'#FFFFFF', primaryText:'#000000', secondaryText:'#666666',
      accent:'#5D3B95', accentSoft:'#8B6BC5', accentPale:'#D5CCEB', divider:'#E0E0E0', iconColor:'#444444'
    },
    fontFamily: { sans:['Lato','system-ui','sans-serif'], heading:['Poppins','system-ui','sans-serif'] }
  } }
};
