module.exports = {
  type: 'react-component',
  npm: {
    esModules: false,
    umd: {
      global: 'Timeline',
      externals: {
        react: 'React'
      }
    }
  }
}
