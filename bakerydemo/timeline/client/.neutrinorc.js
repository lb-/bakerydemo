module.exports = {
  use: [
    "@neutrinojs/airbnb",
    "@neutrinojs/react-components",
    "@neutrinojs/jest",
    neutrino => {
      neutrino.config.when(process.env.NODE_ENV === "production", config => {
        config.externals({
          react: {
            amd: "react",
            commonjs: "react",
            commonjs2: "react",
            root: "React"
          }
        });
      });
    }
  ]
};
