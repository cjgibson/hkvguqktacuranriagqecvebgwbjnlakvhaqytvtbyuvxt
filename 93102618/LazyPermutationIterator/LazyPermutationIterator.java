import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.Iterator;

/**
 * <p>Lazy generator of all permutations over a list of non-primitive Objects, 
 * utilizing the methods outlined in the Steinhaus-Johnson-Trotter
 * algorithm.</p>
 *
 * <p><b>Version 0.1:</b> Utilized dual integer arrays,
 * <i>permutationWeight</i> and <i>permutationDirection</i> to keep track of
 * the weight and direction of each element in the source array.</p>
 *
 * <p><b>Version 0.2:</b> Utilized a single integer array,
 * <i>permutationValue</i>, in place of <i>permutationWeight</i>
 * and <i>permutationDirection</i>. In this new array, an element's sign
 * designates its direction, while its value indicates its weight.<p>
 *
 * <p><b>Version 0.3:</b> Overengineered the code by adding the BigInteger
 * <i>remaining</i> to give the user an idea of how many permutations remained
 * in the LazyPermutationIterator, and to capture the results of <i>factorial<i>,
 * which, in turn, utilizes the BigDecimal class.<p>
 *
 * 
 * 
 * @author  Christian Gibson
 * @see     java.math.BigDecimal
 * @see     java.math.BigInteger
 * @see     java.util.Iterator
 * @version 0.3
 * @date    March 5th, 2015
 * @isodate 2015-03-05T00:00:00-05:00
 */
public class LazyPermutationIterator <T extends Object>
    implements Iterator<T[]> {
    /**
     * Contains the original list of Objects that we're generating all
     * permutations for.
     */
    private T[] source;
    
    /**
     * Integer array responsible for recording the weight and direction of
     * each element in the current permutation of our source array.
     */
    private int[] permutationValue;
    
    /**
     * Integer constants that represent a left and right pointing values in
     * our permutationDirection array. Although DIRECTION_RIGHT is unused in
     * the body of this class, it is included for documentation purposes.
     * ACCURACY represents the number of digits included in 
     * LazyPermutationInterator's BigDecimal _PI and _EN constants.
     */
    private final int DIRECTION_LEFT = -1, DIRECTION_RIGHT = 1, ACCURACY = 587;
    
    /**
     * A boolean flag that monitors if all permutations have been iterated
     * over at any given point of program execution.
     */
    private boolean finished = false;
    
    /**
     * 
     */
    private int length;
    
    /**
     * 
     */
    private BigInteger remaining;
    
    /**
     * 
     */
    private final BigDecimal _00 = new BigDecimal("0"),
                             _01 = new BigDecimal("1"),
                             _02 = new BigDecimal("2"),
                             _10 = new BigDecimal("10"),
                             _12 = new BigDecimal("12"),
                             _PI = new BigDecimal("3.14159265358979323"
                                     + "846264338327950288419716939937"
                                     + "510582097494459230781640628620"
                                     + "899862803482534211706798214808"
                                     + "651328230664709384460955058223"
                                     + "172535940812848111745028410270"
                                     + "193852110555964462294895493038"
                                     + "196442881097566593344612847564"
                                     + "823378678316527120190914564856"
                                     + "692346034861045432664821339360"
                                     + "726024914127372458700660631558"
                                     + "817488152092096282925409171536"
                                     + "436789259036001133053054882046"
                                     + "652138414695194151160943305727"
                                     + "036575959195309218611738193261"
                                     + "179310511854807446237996274956"
                                     + "735188575272489122793818301194"
                                     + "912983367336244065664308602139"
                                     + "494639522473719070217986094370"
                                     + "277053921717629317675238467482"),
                             _EN = new BigDecimal("2.71828182845904523"
                                     + "536028747135266249775724709369"
                                     + "995957496696762772407663035354"
                                     + "759457138217852516642742746639"
                                     + "193200305992181741359662904357"
                                     + "290033429526059563073813232862"
                                     + "794349076323382988075319525101"
                                     + "901157383418793070215408914993"
                                     + "488416750924476146066808226480"
                                     + "016847741185374234544243710753"
                                     + "907774499206955170276183860626"
                                     + "133138458300075204493382656029"
                                     + "760673711320070932870912744374"
                                     + "704723069697720931014169283681"
                                     + "902551510865746377211125238978"
                                     + "442505695369677078544996996794"
                                     + "686445490598793163688923009879"
                                     + "312773617821542499922957635148"
                                     + "220826989519366803318252886939"
                                     + "849646510582093923982948879332");
    
    /**
     * Constructor for a new LazyPermutationIterator object.
     * 
     * @param a The list to generate all permutations for.
     */
    public LazyPermutationIterator(T[] a) {
        if (a.length <= 0) { this.finished = true; }
        this.source = a;
        this.length = this.source.length;
        this.remaining = this.factorial(this.length);
        this.permutationValue = new int[this.length];
        for (int i = 0; i < this.length; i++) {
            this.permutationValue[i] = i + 1;
            this.permutationValue[i] *= this.DIRECTION_LEFT;
        }
    }
    
    /* (non-Javadoc)
     * @see java.util.Iterator#hasNext()
     */
    @Override
    public boolean hasNext() {
        return !this.finished;
    }

    /* (non-Javadoc)
     * @see java.util.Iterator#next()
     */
    @Override
    public T[] next() {
        if (hasNext()) {
            int maxMobileLoc = -1;
            for (int i = 0; i < this.length ; i++) {
                if (isMobile(i)
                    && (maxMobileLoc < 0
                        || this.getWeight(i) > this.getWeight(maxMobileLoc)))
                    maxMobileLoc = i;
            }
            remaining = remaining.subtract(BigInteger.ONE);
            
            if (maxMobileLoc < 0) {
            	assert remaining.equals(BigInteger.ZERO);
                this.finished = true;
                return this.source;
            } else {
                int shift = this.getDirection(maxMobileLoc);
                this.intMove(maxMobileLoc, shift, this.permutationValue);
                maxMobileLoc += shift;
                
                if (maxMobileLoc < this.length
                    && maxMobileLoc > -1) {
                    for (int i = 0 ; i < this.length ; i++) {
                        if (this.getWeight(i) > this.getWeight(maxMobileLoc))
                            swapDirections(i);
                    }
                }
                
                return mapPermutation();
            }
        } else {
            return null;
        }
    }

    /* (non-Javadoc)
     * @see java.util.Iterator#remove()
     */
    @Override
    public void remove() {
        return;
    }
    
    /**
     * @return
     */
    private T[] mapPermutation() {
        T[] mappedPermutation = (T[]) new Object[this.length];
        for (int i = 0; i < this.length; i++) {
            mappedPermutation[i] = this.source[this.getWeight(i) - 1];
        }
        return mappedPermutation;
    }
    
    /**
     * @param loc
     * @return
     */
    private boolean isMobile(int loc) {
        int direction = this.getDirection(loc);
        int weight = this.getWeight(loc);
        if (direction + loc < this.length
            && direction + loc > -1) {
            if (this.getWeight(direction + loc) < weight) {
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }
    
    /**
     * @param a
     * @param move
     * @param array
     */
    private void intMove(int i, int move, int[] array) {
        int temp = array[i];
        array[i] = array[i+move];
        array[i+move] = temp;
    }
    
    /**
     * @param a
     */
    private void swapDirections(int i) {
        this.permutationValue[i] *= -1;
    }
    
    
    /**
     * @param i
     * @return
     */
    public int getWeight(int i) {
        return this.permutationValue[i] * sign(this.permutationValue[i]);
    }
    
    /**
     * @param i
     * @return
     */
    public int getDirection(int i) {
        return sign(this.permutationValue[i]);
    }
    
    /**
     * @param n
     * @return
     */
    public int sign(int n) {
        return (n < 0) ? -1 : 1;
    }
    
    /**
     * @param i
     * @return
     */
    public BigInteger factorial(int i) {
    	i += 1;
        BigDecimal input = new BigDecimal(i);
        // sqrt(2 * PI / i);
        BigDecimal aprx1 = _02.multiply(_PI.divide(input));
        aprx1 = this.sqrt(aprx1, this.ACCURACY);
        // pow(i + 1 / ( 12 * i - 1 / (10 * i) ) / E ), i);
        BigDecimal aprx2 = input.add(
                _01.divide(
                    _12.multiply(
                        input.subtract(
                            _01.divide(
                                _10.multiply(
                                    input
                                ),
                                this.ACCURACY,
                                BigDecimal.ROUND_HALF_UP))
                    ),
                	this.ACCURACY,
                	BigDecimal.ROUND_HALF_UP));
        aprx2 = aprx2.divide(_EN, this.ACCURACY, BigDecimal.ROUND_HALF_UP);
        aprx2 = aprx2.pow(i);
        // sqrt(2 * PI / i) * pow(i + 1 / ( 12 * i - 1 / (10 * i) ) / E ), i);
        return aprx1.multiply(aprx2).toBigInteger();
    }
    
    /**
     * @param n
     * @param scale
     * @return
     */
    public BigDecimal sqrt(BigDecimal n, final int scale) {
        BigDecimal aprx = _00;
        BigDecimal root = new BigDecimal(Math.sqrt(n.doubleValue()));
        while (!root.equals(aprx)) {
            aprx = root;
            root = n.divide(aprx, scale, BigDecimal.ROUND_HALF_UP);
            root = root.add(aprx);
            root = root.divide(_02, scale, BigDecimal.ROUND_HALF_UP);
        }
        return root;
    }
    
    /* (non-Javadoc)
     * @see java.lang.Object#toString()
     */
    public String toString() {
        return "";
    }
    
    /**
     * @param width
     * @return
     */
    public String toString(int width) {
        return "";
    }
}
