/* eslint-disable */
interface String {
    /**
     * Get domain from an URL string
     */
    domain(): string;
}

String.prototype.domain = function () {
    return this.split('/').slice(0, 3).join('/');
};
