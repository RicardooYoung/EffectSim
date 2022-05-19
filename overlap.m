function add_rain(image_path, image_name, mask_path, rain_path)
    img = imread(image_path);
    img = im2double(img);
    fre = fft2(img);
    clear img
    am = abs(fre);
    aa = angle(fre);
    len = size(fre);
    len = len(1);
    clear fre
    x = linspace(0, len-1, len);
    I0 = trapz(x, trapz(x, am, 2));
    mask = imread(mask_path);
    mask = im2double(mask);
    mask = rgb2gray(mask);
    mask_fre = fft2(mask);
    mask_am = abs(mask_fre);
    mask_am = log(abs(mask_am)+1);
    mask_am = mask_am ./ max(max(max(mask_am)));
    temp_am = am .* mask_am;
    I1 = trapz(x, trapz(x, temp_am, 2));
    temp_am = temp_am .* I0 ./ I1;
    fr1 = temp_am .* exp(1i.*aa);
    img1 = real(ifft2(fr1));
    img1 = img1 / max(max(max(img1)));
    imwrite(img1, [rain_path, '/', image_name '.jpg'])
