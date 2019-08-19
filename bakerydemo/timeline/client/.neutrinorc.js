module.exports = {
  use: [
    "@neutrinojs/airbnb",
    ["@neutrinojs/react-components", { mains: 'fff'}]
    // [
    //   "@neutrinojs/react-components",
    //   {
    //     // babel: {
    //     //   // Override options for babel-preset-env:
    //     //   presets: [
    //     //     [
    //     //       "babel-preset-env",
    //     //       {
    //     //         modules: false,
    //     //         useBuiltIns: true,
    //     //         exclude: [
    //     //           "transform-regenerator",
    //     //           "transform-async-to-generator"
    //     //         ]
    //     //       }
    //     //     ]
    //     //   ]
    //     // }
    //     babel: {
    //       presets: [],
    //     },
    //     options: {
    //       babel: {
    //         presets: [],
    //       },
    //       // target: 'web'
    //       externals: {
    //         'BAZ': "BAR"
    //     //     react: {
    //     //       // commonjs: 'lodash',
    //     //       // amd: 'lodash',
    //     //       root: "_" // indicates global variable
    //     //     }
    //       }
    //     }
    //   }
    // ],
    // "@neutrinojs/jest",
    // function(options) {return {}}
    // ["@neutrinojs/library", { name: 'Logger' }]
  ]
};
