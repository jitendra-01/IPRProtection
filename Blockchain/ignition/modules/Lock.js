// This setup uses Hardhat Ignition to manage smart contract deployments.
// Learn more about it at https://hardhat.org/ignition

const { buildModule } = require("@nomicfoundation/hardhat-ignition/modules");
// const hre = require("hardhat");

// async function main() {
//   const signer = await hre.ethers.getSigners();
//   const deployer = signer[0];
//   console.log(await deployer.provider.getBalance());
// }
// main();
module.exports = buildModule("LockModule", (m) => {
  const lock = m.contract("PatentRegistry")

  return { lock };
});