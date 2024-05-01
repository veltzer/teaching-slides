// Export a configuration object
module.exports = {
  // Set the theme to 'material'
  theme: 'material',

  // Set the output format and filename
  output: 'presentation.pdf',

  // Configure options
  options: {
    // Enable syntax highlighting for specific languages
    highlight: ['javascript', 'typescript'],

    // Set the presentation mode (options: 'reveal' or 'fullpage')
    mode: 'fullpage',

    // Set presentation margins (in pixels)
    margin: [50, 30, 40, 50],
  },

  // Add custom plugins (replace with actual plugin names and paths)
  plugins: [
    require('path/to/your-custom-plugin'),
    require('path/to/another-plugin'),
  ],
};
