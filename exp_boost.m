function add_rain(image_path, image_name, rain_path, alpha)
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
    weight = ones(len);
    for i = 1:len
        for j = 1:len
            weight(i, j) = ...
                alpha^(abs(i + j - len) / len * 2);
        end
    end
    temp_am = am .* weight;
    I1 = trapz(x, trapz(x, temp_am, 2));
    temp_am = temp_am .* I0 ./ I1;
    % Keep energy same
    fr1 = temp_am .* exp(1i.*aa);
    img1 = real(ifft2(fr1));
    img1 = img1 / max(max(max(img1)));
    imwrite(img1, [rain_path, '/', image_name '.jpg'])
