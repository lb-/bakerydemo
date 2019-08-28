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
        //   // https://github.com/neutrinojs/neutrino/blob/master/packages/react-components/index.js#L62
        //   // https://www.npmjs.com/package/webpack-node-externals
        //   // https://webpack.js.org/configuration/externals/#externals
        //   // https://github.com/neutrinojs/neutrino/issues/1425
        //   // https://github.com/liady/webpack-node-externals/issues/17
        //   importType: "root",
        //   whitelist: ["interactjs", "moment", "react-calendar-timeline"]
        //   // whitelist: ["react-calendar-timeline"]
        //   // externals: {
        //   //   react: "React"
        //   // }
        // },
        // externals: false // this bundles even React with everything
      }
    ],
    "@neutrinojs/jest",
    // [
    //   "@neutrinojs/library",
    //   {
    //     name: "reduxExample",
    //     externals: {
    //       whitelist: ["moment", "react-calendar-timeline"]
    //     }
    //   }
    // ]
    neutrino => {
      console.log("neutrino", neutrino);
      return neutrino;
    }
  ]
};
