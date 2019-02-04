import { BasePredicate, testSymbol } from './base-predicate';
import { Ow } from '../..';
/**
 * @hidden
 */
export declare class AnyPredicate<T = any> implements BasePredicate<T> {
    private readonly predicates;
    constructor(predicates: BasePredicate[]);
    [testSymbol](value: T, main: Ow): void;
}
