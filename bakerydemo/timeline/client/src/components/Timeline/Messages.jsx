import React from 'react';
import PropTypes from 'prop-types';

/**
 * A verbose example of a Functional component. Messages renders the loading or
 * error message states.
 * @param {Object} props
 */
const Messages = ({ error, isLoading }) => (
  <div className="messages">
    <ul>
      {isLoading && <li className="success">Loading...</li>}
      {error && (
        <li className="error">
          <span>Error: </span>
          {error.message}
        </li>
      )}
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
