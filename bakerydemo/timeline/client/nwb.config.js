module.exports = {
  devServer: {
    proxy: {
      '/api': 'http://localhost:8000', // Wagtail dev server
    },
  },
  type: 'react-component',
  npm: {
    esModules: false,
    umd: {
      global: 'Timeline',
      externals: {
        react: 'React',
      },
    },
  },
  webpack: {
    extractCSS: {
      filename:
        process.env.NODE_ENV === 'production' ? '[name].css' : '[name].css', // remove hash from production build css
    },
  },
};
