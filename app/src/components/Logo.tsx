import Image from "next/image";

export default function Logo() {
  return (
    <div className="relative">
      <div className="absolute top-0 right-0">
        <Image src="/mock-logo.svg" alt="Logo" height={100} width={100} />
      </div>
    </div>
  );
}
