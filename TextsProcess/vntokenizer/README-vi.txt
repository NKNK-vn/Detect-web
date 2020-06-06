
Chương trình tách từ vnTokenizer, version 4.1.1.
================================================

(Release 28/12/2009).


I) TỔNG QUAN
-------------

	+) Chương trình vnTokenizer được sử dụng để tách từ các văn bản tiếng Việt (mã hóa bằng bảng mã Unicode UTF-8).
	
	+) Chương trình chạy dưới dạng dòng lệnh:
	 
		- vnTokenizer.sh nếu chạy trên các hệ điều hành Linux/Unix/Mac OS
		- vnTokenizer.bat nếu chạy trên các hệ điều hành MS Windows
		
	+) Yêu cầu: Máy cần cài JRE (Java Runtime Environment) phiên bản 1.6. JRE có thể tải về từ địa chỉ  website 
			Java của Sun Microsystems: http://java.sun.com/
	
II) DỮ LIỆU
------------

	Trong một lần chạy vnTokenizer có thể tách từ một tệp hoặc đồng thời nhiều tệp nằm trong cùng một thư mục. 
	
	1) Tách từ một tệp:
	
		+) Dữ liệu cần cung cấp cho chương trình gồm 1 tệp văn bản tiếng Việt, dạng thô (ví dụ như tệp README.txt này).
			  
		+) Kết quả: Một tệp văn bản kết quả tách từ được ghi dưới định dạng đơn giản hoặc định dạng XML, tùy 
			theo lựa chọn của người sử dụng (xem ví dụ dưới đây). 
				
			
	2) Tách từ nhiều tệp nằm trong một thư mục:
	
		+) Dữ liệu cần cung cấp gồm một thư mục chứa các tệp văn bản thô cần tách từ (thư mục input) và một thư mục trống 
			(thư mục output) để chứa kết quả tách từ.
		
		+) Mặc định, chương trình sẽ tự động quét toàn bộ thư mục input và lọc ra tất cả các tệp có đuôi là ".txt".  
			 Người sử dụng có thể thay đổi đuôi mặc định này thành đuôi bất kì, ví dụ ".seg" bằng tùy chọn -e của dòng lệnh 
			 (xem ví dụ dưới đây). 
			 
		+) Kết quả: Tập các tệp kết quả tách từ trong thư mục output, các tệp này có cùng tên với tệp input tương ứng, 
			tức là tệp input/abc.txt sẽ có kết quả là tệp output/abc.txt.  
		  
		
III) CHẠY CHƯƠNG TRÌNH
-----------------------
			
	1) Tách từ một tệp:
	
			vnTokenizer.sh -i <tệp-input> -o <tệp-output> [<các-tùy-chọn>]
		
			Hai tùy chọn -i và -o là bắt buộc. Ngoài ra, người dùng có thể cung cấp các tùy chọn không bắt buộc sau đây:
			
			+) -xo : dùng định dạng XML để biểu diễn kết quả thay vì định dạng mặc định là văn bản thô.
			  
			+) -nu : không sử dụng dấu gạch dưới (no underscore) khi ghi kết quả. Nếu tùy chọn này được sử dụng thì trong 
					kết quả, các âm tiết không được nối với nhau bằng ký tự gạch dưới, mà bằng ký tự trắng.
			
			+) -sd : sử dụng mô-đun tách câu trước khi thực hiện tách từ. Nếu tùy chọn này được sử dụng thì trước tiên 
					vnTokenizer thực hiện tách văn bản input thành một tập các câu, sau đó thực hiện tách từ từng câu một.
					Mặc định thì mô-đun tách câu không được sử dụng, vnTokenizer thực hiện tách từ trên toàn bộ văn bản.

			Các tùy chọn này có thể được phối hợp đồng thời với nhau để cho ra kết quả mong muốn. 
		
		Ví dụ: 
		
			a) vnTokenizer.sh -i samples/test0.txt -o samples/test0.tok.txt
				
				Tách từ tệp samples/test0.txt và ghi kết quả vào tệp samples/test0.tok.txt
				
			b) vnTokenizer.sh -i samples/test0.txt -o samples/test0.tok.xml -xo
				
				Tương tự như a), tuy nhiên tệp kết quả samples/test0.tok.xml sẽ có định dạng XML.
				
			c) vnTokenizer.sh -i samples/test0.txt -o samples/test0.tok.txt -sd 
				
				Tương tự như a) và sử dụng mô-đun tách câu trước khi tách từ.
	
	2) Tách từ một thư mục:
			
		Ngoài các tùy chọn như ở trên, khi tách từ thư mục, chương trình cung cấp thêm tùy chọn không bắt buộc
			  
				+) -e : chỉ định phần mở rộng của các tệp cần tách.
	 
	 	Ví dụ: 
	 	
	 		a) vnTokenizer.sh -i samples/input -o samples/output
	 		
	 			Thực hiện tách từ tất cả các tệp samples/input/*.txt, ghi kết quả ra thư mục samples/output. 
	 		
	 		b) vnTokenizer.sh -i samples/input -o samples/output -e .xyz
	 		 
	 		 	Thực hiện tách từ tất cả các tệp samples/input/*.xyz, ghi kết quả ra thư mục samples/output.
	 		 

IV)  XEM THÊM
--------------
	Thư mục resources và tệp CHANGES.txt.

V) LIÊN HỆ
------------

	- Lê Hồng Phương <phuonglh@gmail.com>
	- Nguyễn Thị Minh Huyền <ntmhuyen@gmail.com>
	
	Khoa Toán-Cơ-Tin học, Trường Đại học Khoa học Tự nhiên, ĐHQG Hà Nội, Việt Nam.
	
	Website: http://www.loria.fr/~lehong/tools/vnTokenizer.php