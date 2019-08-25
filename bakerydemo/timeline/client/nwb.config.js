module.exports = {
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
