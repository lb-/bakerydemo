module.exports = {
  options: {
    // output: '../../static/timeline/dist' // Override to absolute directory in django static folder
    // externals: {
    //   whitelist: ["moment", "react-calendar-timeline"]
    // }
  },
  use: [
    "@neutrinojs/airbnb",
    [
      "@neutrinojs/react-components",
      {
        // name: "HelloWorld",
        // externals: {
        // whitelist: ["moment", "react-calendar-timeline"]
        // whitelist: ["react-calendar-timeline"]
        // }
      }
    ],
    "@neutrinojs/jest"
    // [
    //   "@neutrinojs/library",
    //   {
    //     name: "reduxExample",
    //     externals: {
    //       whitelist: ["moment", "react-calendar-timeline"]
    //     }
    //   }
    // ]
  ]
};
