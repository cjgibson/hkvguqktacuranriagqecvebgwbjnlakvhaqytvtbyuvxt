import java.util.Arrays;

public class main {
	public static void main(String[] args) {
		for (int i = 3 ; i < 6 ; i++) {
			Integer[] test = range(i);
			int count = 0;
			LazyPermutationIterator<Integer> lazy = 
					new LazyPermutationIterator<Integer>(test);
			System.out.printf("Permutations of array of size %d (expected %d)",
					i, lazy.factorial(i));
			while (lazy.hasNext()) {
				count += 1;
				System.out.println();
				System.out.printf("%d: ", count);
				System.out.print(Arrays.toString( lazy.next() ));
			}
			System.out.println("\n");
		}
	}
	
	public static Integer[] range(int i) {
		Integer[] ret = new Integer[i];
		for (int j = 0 ; j < i ; j++) {
			ret[j] = j+1;
		}
		return ret;
	}
}
