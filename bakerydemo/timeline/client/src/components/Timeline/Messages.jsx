import React from 'react'; // eslint-disable-line import/no-extraneous-dependencies
import PropTypes from 'prop-types'; // eslint-disable-line import/no-extraneous-dependencies

/**
 * A verbose example of a Functional component. Messages renders the loading or
 * error message states.
 * @param {Object} props
 */
const Messages = ({ error, isLoading }) => (
  <div className="messages">
    <ul>
      {isLoading && <li className="success">Loading...</li>}
      {error && <li className="error">Error: {error.message}</li>}
    </ul>
  </div>
);

Messages.defaultProps = {
  isLoading: false,
  error: {},
};

Messages.propTypes = {
  isLoading: PropTypes.bool,
  error: PropTypes.shape({
    message: PropTypes.string,
  }),
};

export default Messages;
